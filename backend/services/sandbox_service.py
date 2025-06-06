# サンドボックスサービス - 完全版
import asyncio
import docker
import time
from typing import Optional
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
import nbformat


def notebook_to_python(notebook_str: str) -> str:
    """Jupyter Notebook文字列からPythonコードを抽出する"""
    nb = nbformat.reads(notebook_str, as_version=4)
    code_cells = [cell.source for cell in nb.cells if cell.cell_type == "code"]
    return "\n\n".join(code_cells)


class CodeExecutionResult(BaseModel):
    stdout: str
    stderr: str
    execution_time_ms: float
    exit_code: int
    error_type: Optional[str] = None
    succeeded: bool


def execute_python_code_sync(
    user_code: str, stdin_input: Optional[str] = None
) -> CodeExecutionResult:
    """
    Dockerコンテナ内でPythonコードを同期的に実行する関数
    """
    start_time = time.time()

    def run_container():
        """コンテナ実行を行う内部関数"""
        client = docker.from_env()

        try:
            # 標準入力がある場合はそれを含めたコードを作成
            if stdin_input:
                # 標準入力をハードコーディングしたコードを生成
                full_code = f"""
import sys
from io import StringIO
sys.stdin = StringIO('''{stdin_input}''')

{user_code}
"""
            else:
                full_code = user_code

            # コンテナを実行（コードを直接実行）
            result = client.containers.run(
                image="python-sandbox",
                command=["python", "-c", full_code],
                network_disabled=True,
                mem_limit="128m",
                remove=True,
                stderr=True,
                stdout=True,
            )

            stdout = result.decode("utf-8") if result else ""
            stderr = ""
            exit_code = 0

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
        # タイムアウト付きでコンテナを実行
        with ThreadPoolExecutor() as executor:
            future = executor.submit(run_container)
            try:
                stdout, stderr, exit_code = future.result(timeout=5)
            except FuturesTimeoutError:
                stdout = ""
                stderr = "Code execution timed out (5 seconds)"
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
