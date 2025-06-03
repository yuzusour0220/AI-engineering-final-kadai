#!/usr/bin/env python3
"""
同期版のサンドボックステスト
"""

import docker
import tempfile
import time
import os
from typing import Optional


def execute_python_code_sync(user_code: str) -> dict:
    """同期版のコード実行関数"""
    start_time = time.time()

    try:
        print(f"コード実行開始: {repr(user_code[:50])}...")

        # Dockerクライアントを初期化
        client = docker.from_env()
        print("Dockerクライアント初期化完了")

        # 一時ファイルにユーザーコードを書き込み
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write(user_code)
            temp_file_path = temp_file.name

        print(f"一時ファイル作成: {temp_file_path}")

        try:
            print("コンテナ実行中...")
            # コンテナを実行
            result = client.containers.run(
                image="python:3.11-slim",
                command=["python", "/tmp/user_code.py"],
                volumes={temp_file_path: {"bind": "/tmp/user_code.py", "mode": "ro"}},
                network_disabled=True,
                mem_limit="128m",
                remove=True,
                stderr=True,
                stdout=True,
                timeout=10,
            )

            print(f"コンテナ実行完了、結果型: {type(result)}")

            stdout = result.decode("utf-8") if result else ""
            stderr = ""
            exit_code = 0

            print(f"stdout: {repr(stdout)}")

        except docker.errors.ContainerError as e:
            print(f"ContainerError: exit_status={e.exit_status}")
            stdout = e.stdout.decode("utf-8") if e.stdout else ""
            stderr = e.stderr.decode("utf-8") if e.stderr else ""
            exit_code = e.exit_status
            print(f"stdout: {repr(stdout)}")
            print(f"stderr: {repr(stderr)}")

        except Exception as e:
            print(f"例外: {e}")
            import traceback

            traceback.print_exc()
            stdout = ""
            stderr = f"Execution error: {str(e)}"
            exit_code = 1

        execution_time = (time.time() - start_time) * 1000

        result_dict = {
            "stdout": stdout,
            "stderr": stderr,
            "execution_time_ms": execution_time,
            "exit_code": exit_code,
            "succeeded": exit_code == 0 and not stderr.strip(),
        }

        print(f"結果: {result_dict}")
        return result_dict

    except Exception as e:
        print(f"全体エラー: {e}")
        import traceback

        traceback.print_exc()
        execution_time = (time.time() - start_time) * 1000
        return {
            "stdout": "",
            "stderr": f"Unexpected error: {str(e)}",
            "execution_time_ms": execution_time,
            "exit_code": 1,
            "succeeded": False,
        }

    finally:
        # 一時ファイルを削除
        try:
            if "temp_file_path" in locals() and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                print("一時ファイル削除完了")
        except Exception as e:
            print(f"一時ファイル削除エラー: {e}")


def main():
    print("=== 同期版サンドボックステスト ===")

    # テスト1: 基本的なprint
    print("\nテスト1: 基本的なprint")
    result1 = execute_python_code_sync('print("Hello, World!")')

    # テスト2: 計算
    print("\nテスト2: 計算")
    result2 = execute_python_code_sync("print(1 + 2 + 3)")

    # テスト3: エラー
    print("\nテスト3: エラー")
    result3 = execute_python_code_sync("print(1/0)")

    print("\n=== テスト完了 ===")


if __name__ == "__main__":
    main()
