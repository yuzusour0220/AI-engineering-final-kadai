# サンドボックスサービス - 完全版
import asyncio
import docker
import time
import json
import re
import logging
from typing import Optional, List
from pathlib import Path
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
import nbformat

logger = logging.getLogger(__name__)

# パス設定: サンドボックス用Dockerfileディレクトリ
SANDBOX_DOCKER_PATH = Path(__file__).resolve().parent.parent / "sandbox_docker"


def notebook_to_python(notebook_str: str) -> str:
    """Jupyter Notebook文字列からPythonコードを抽出する"""
    try:
        # VSCode形式のXMLnotebookかどうかをチェック
        if notebook_str.strip().startswith("<"):
            # XMLベースのVSCode notebook形式の処理
            import re

            # VSCode.Cellタグからコードセルを抽出
            code_pattern = (
                r'<VSCode\.Cell[^>]*language="python"[^>]*>(.*?)</VSCode\.Cell>'
            )
            matches = re.findall(code_pattern, notebook_str, re.DOTALL)

            code_cells = []
            for match in matches:
                # HTMLエンティティをデコードし、余分な空白を削除
                cell_content = match.strip()
                if cell_content:
                    code_cells.append(cell_content)

            return "\n\n".join(code_cells)

        # JSONベースのJupyter notebook形式の処理
        # まず、文字列レベルでnull値を修正し、制御文字も除去
        import re

        # 制御文字を除去（改行とタブは保持）
        cleaned_notebook_str = re.sub(
            r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", notebook_str
        )

        # null値を適切な値に置き換え
        cleaned_notebook_str = cleaned_notebook_str.replace(
            '"execution_count": null', '"execution_count": 0'
        )
        cleaned_notebook_str = cleaned_notebook_str.replace(
            '"outputs": null', '"outputs": []'
        )
        cleaned_notebook_str = cleaned_notebook_str.replace(
            '"metadata": null', '"metadata": {}'
        )

        notebook_dict = json.loads(cleaned_notebook_str)

        # 念のため、辞書レベルでもnull値を処理
        if "cells" in notebook_dict:
            for cell in notebook_dict["cells"]:
                if "execution_count" in cell and cell["execution_count"] is None:
                    cell["execution_count"] = 0
                if "outputs" in cell and cell["outputs"] is None:
                    cell["outputs"] = []
                # metadataのnull値も処理
                if "metadata" in cell and cell["metadata"] is None:
                    cell["metadata"] = {}

        # nbformatで再度パース
        nb = nbformat.from_dict(notebook_dict)
        code_cells = []
        for cell in nb.cells:
            if cell.cell_type == "code":
                # sourceがリストの場合は結合、文字列の場合はそのまま使用
                if isinstance(cell.source, list):
                    # リストの場合、各行を結合（改行文字がない場合は追加）
                    cell_code = "".join(
                        line if line.endswith("\n") else line + "\n"
                        for line in cell.source
                    ).rstrip("\n")
                    code_cells.append(cell_code)
                else:
                    code_cells.append(cell.source)
        return "\n\n".join(code_cells)

    except (json.JSONDecodeError, KeyError, Exception) as e:
        # フォールバック: より簡単な抽出方法を試す
        try:
            # 直接正規表現でコードセルを抽出
            import re

            # JSONのsourceフィールドを直接抽出
            pattern = r'"cell_type":\s*"code".*?"source":\s*(\[.*?\])'
            matches = re.findall(pattern, notebook_str, re.DOTALL)

            code_cells = []
            for match in matches:
                try:
                    # JSON配列として解析
                    source_lines = json.loads(match)
                    if isinstance(source_lines, list):
                        code_cells.append("".join(source_lines))
                    else:
                        code_cells.append(str(source_lines))
                except:
                    continue

            if code_cells:
                return "\n\n".join(code_cells)

            # 最後の手段: nbformatを使用
            nb = nbformat.reads(notebook_str, as_version=4)
            code_cells = []
            for cell in nb.cells:
                if cell.cell_type == "code":
                    if isinstance(cell.source, list):
                        # リストの場合、各行を結合（改行文字がない場合は追加）
                        cell_code = "".join(
                            line if line.endswith("\n") else line + "\n"
                            for line in cell.source
                        ).rstrip("\n")
                        code_cells.append(cell_code)
                    else:
                        code_cells.append(cell.source)
            return "\n\n".join(code_cells)
        except Exception:
            raise Exception(f"Failed to parse notebook: {str(e)}")


class CodeExecutionResult(BaseModel):
    stdout: str
    stderr: str
    execution_time_ms: float
    exit_code: int
    error_type: Optional[str] = None
    succeeded: bool


def ensure_sandbox_image(client: docker.DockerClient) -> None:
    """Ensure the sandbox image exists; build it if missing."""
    try:
        client.images.get("python-sandbox")
    except docker.errors.ImageNotFound:
        logger.info("python-sandbox image not found. Building...")
        client.images.build(path=str(SANDBOX_DOCKER_PATH), tag="python-sandbox")
    except Exception as exc:  # pragma: no cover - best effort logging
        logger.warning("Failed to verify sandbox image: %s", exc)


def execute_python_code_sync(
    user_code: str, stdin_input: Optional[str] = None
) -> CodeExecutionResult:
    """
    Dockerコンテナ内でPythonコードを同期的に実行する関数
    """
    start_time = time.time()

    def validate_package_name(package: str) -> bool:
        """パッケージ名の安全性を検証"""
        # 基本的なパッケージ名パターンの検証
        if not re.match(r"^[a-zA-Z0-9\-_\.]+([<>=!]+[a-zA-Z0-9\-_\.]+)*$", package):
            return False

        # 危険なパッケージ名のブラックリスト
        dangerous_patterns = [
            r"\.\./",  # パストラバーサル
            r"[;&|]",  # コマンドインジェクション
            "sudo",  # 権限昇格
            "rm",  # ファイル削除
            "chmod",  # 権限変更
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, package, re.IGNORECASE):
                return False

        return True

    def extract_pip_packages(code: str) -> List[str]:
        """コードから pip install が必要なライブラリ名を抽出"""
        # !pip install パターン (Jupyter Notebook風)
        pip_pattern = r"^!pip install\s+(.+)"
        # pip install パターン (通常のスクリプト)
        pip_pattern2 = r"^pip install\s+(.+)"

        matches = re.findall(pip_pattern, code, re.MULTILINE)
        matches.extend(re.findall(pip_pattern2, code, re.MULTILINE))

        packages = []
        for match in matches:
            # パッケージ名をスペースで分割して個別のパッケージとして追加
            # バージョン指定やオプションも含めて適切に処理
            parts = match.strip().split()
            for part in parts:
                # オプション（--upgrade, --quiet等）をスキップ
                if not part.startswith("-"):
                    packages.append(part)

        # 重複を除去し、安全なパッケージ名のみを許可
        safe_packages = []
        for pkg in set(packages):
            # セキュリティ検証
            if validate_package_name(pkg):
                safe_packages.append(pkg)
            else:
                logger.warning("Potentially unsafe package name rejected: %s", pkg)

        return safe_packages

    def remove_pip_install_lines(code: str) -> str:
        """コードから !pip install と pip install の行を削除"""
        # !pip install パターン
        pip_pattern1 = r"^!pip install\s+.+$"
        # pip install パターン
        pip_pattern2 = r"^pip install\s+.+$"

        code = re.sub(pip_pattern1, "", code, flags=re.MULTILINE)
        code = re.sub(pip_pattern2, "", code, flags=re.MULTILINE)

        return code

    def run_container():
        """コンテナ実行を行う内部関数"""
        client = docker.from_env()

        # イメージが無ければ自動でビルド
        ensure_sandbox_image(client)

        try:
            # pip install が必要なライブラリを抽出
            pip_packages = extract_pip_packages(user_code)
            # pip install 行を削除したコードを作成
            cleaned_code = remove_pip_install_lines(user_code)

            # 標準入力がある場合はそれを含めたコードを作成
            if stdin_input:
                # 標準入力をハードコーディングしたコードを生成
                full_code = f"""
import sys
from io import StringIO
sys.stdin = StringIO('''{stdin_input}''')

{cleaned_code}
"""
            else:
                full_code = cleaned_code

            # コンテナを起動
            container = client.containers.run(
                image="python-sandbox",
                command=["sleep", "30"],  # 一時的にsleepで起動
                network_disabled=True,
                mem_limit="128m",
                detach=True,
            )

            try:
                # 変数を初期化
                stderr = ""

                # 必要なライブラリをインストール
                if pip_packages:
                    logger.info("Installing packages: %s", pip_packages)
                    installed_packages = []
                    failed_packages = []

                    for package in pip_packages:
                        try:
                            # より詳細なインストールオプション
                            install_result = container.exec_run(
                                [
                                    "pip",
                                    "install",
                                    "--no-cache-dir",
                                    "--disable-pip-version-check",
                                    "--quiet",
                                    package,
                                ],
                                stdout=True,
                                stderr=True,
                            )

                            if install_result.exit_code == 0:
                                installed_packages.append(package)
                                logger.info("Successfully installed: %s", package)
                            else:
                                failed_packages.append(package)
                                error_msg = (
                                    install_result.output.decode("utf-8")
                                    if install_result.output
                                    else "Unknown error"
                                )
                                logger.warning("Failed to install package %s: %s", package, error_msg)

                        except Exception as e:
                            failed_packages.append(package)
                            logger.warning("Exception during package installation %s: %s", package, str(e))

                    # インストール結果をログに記録
                    if installed_packages:
                        logger.info("Successfully installed packages: %s", installed_packages)
                    if failed_packages:
                        logger.warning("Failed to install packages: %s", failed_packages)
                        # 失敗したパッケージがあることをstderrに記録（ユーザーに通知）
                        if not stderr:
                            stderr = f"Warning: Could not install some packages: {', '.join(failed_packages)}\n"

                # 実際のコードを実行
                exec_result = container.exec_run(["python", "-c", full_code])

                stdout = (
                    exec_result.output.decode("utf-8") if exec_result.output else ""
                )
                # exit_codeが0でない場合はstdoutをstderrとして扱う
                if exec_result.exit_code != 0:
                    stderr = stdout
                    stdout = ""

                exit_code = exec_result.exit_code

            finally:
                # コンテナを停止・削除
                container.stop()
                container.remove()

        except docker.errors.ContainerError as e:
            # Docker SDK 7.1.0 での ContainerError 処理
            stdout = ""  # ContainerError時はstdoutは空
            stderr = e.stderr.decode("utf-8") if e.stderr else ""
            exit_code = e.exit_status

        except Exception as e:
            # その他のDocker関連エラー
            stdout = ""
            stderr = f"Docker error: {str(e)}"
            exit_code = 1

        return stdout, stderr, exit_code

    try:
        # タイムアウト付きでコンテナを実行（30秒に延長してパッケージインストールに対応）
        with ThreadPoolExecutor() as executor:
            future = executor.submit(run_container)
            try:
                stdout, stderr, exit_code = future.result(timeout=30)
            except FuturesTimeoutError:
                stdout = ""
                stderr = "Code execution timed out (30 seconds)"
                exit_code = 124

        # 実行時間を計算
        execution_time = (time.time() - start_time) * 1000

        # エラータイプを判定
        error_type = None
        if exit_code != 0:
            if exit_code == 124:
                error_type = "TimeoutError"
            elif "SyntaxError" in stderr:
                error_type = "SyntaxError"
            elif "NameError" in stderr:
                error_type = "NameError"
            elif "TypeError" in stderr:
                error_type = "TypeError"
            elif "ValueError" in stderr:
                error_type = "ValueError"
            elif "IndexError" in stderr:
                error_type = "IndexError"
            elif "KeyError" in stderr:
                error_type = "KeyError"
            elif "ZeroDivisionError" in stderr:
                error_type = "ZeroDivisionError"
            else:
                error_type = "RuntimeError"

        # 成功判定
        succeeded = exit_code == 0 and not stderr.strip()

        return CodeExecutionResult(
            stdout=stdout,
            stderr=stderr,
            execution_time_ms=execution_time,
            exit_code=exit_code,
            error_type=error_type,
            succeeded=succeeded,
        )

    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        return CodeExecutionResult(
            stdout="",
            stderr=f"Unexpected error: {str(e)}",
            execution_time_ms=execution_time,
            exit_code=1,
            error_type="UnexpectedError",
            succeeded=False,
        )


async def execute_python_code_in_docker(
    user_code: str, stdin_input: Optional[str] = None
) -> CodeExecutionResult:
    """
    Dockerコンテナ内でPythonコードを非同期で実行する関数
    """
    # 同期関数を非同期で実行
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, execute_python_code_sync, user_code, stdin_input
    )
