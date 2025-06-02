#!/usr/bin/env python3
"""
サンドボックスサービスの簡単なテスト
"""

import docker
import tempfile
import os
import sys


def test_docker_basic():
    """基本的なDockerテスト"""
    try:
        print("1. Dockerクライアントの初期化...")
        client = docker.from_env()
        print("   ✓ Dockerクライアント初期化完了")

        print("2. 一時ファイルの作成...")
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write('print("Hello from Docker!")')
            temp_file_path = temp_file.name
        print(f"   ✓ 一時ファイル作成完了: {temp_file_path}")

        print("3. Dockerコンテナの実行...")
        try:
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
            print(f"   ✓ コンテナ実行完了")
            print(f"   結果の型: {type(result)}")

            if isinstance(result, bytes):
                decoded = result.decode("utf-8")
                print(f"   stdout: '{decoded}'")
            else:
                print(f"   結果: {result}")

        except docker.errors.ContainerError as e:
            print(f"   ❌ コンテナエラー:")
            print(f"   exit_status: {e.exit_status}")
            print(f"   stdout: {e.stdout}")
            print(f"   stderr: {e.stderr}")
        except Exception as e:
            print(f"   ❌ 予期しないエラー: {e}")
            import traceback

            traceback.print_exc()

        finally:
            print("4. クリーンアップ...")
            try:
                os.unlink(temp_file_path)
                print("   ✓ 一時ファイル削除完了")
            except Exception as e:
                print(f"   ❌ 一時ファイル削除エラー: {e}")

    except Exception as e:
        print(f"❌ テスト失敗: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    print("=== Docker Basic Test ===")
    success = test_docker_basic()
    print(f"\nテスト結果: {'成功' if success else '失敗'}")
    sys.exit(0 if success else 1)
