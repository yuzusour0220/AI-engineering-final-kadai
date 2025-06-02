#!/usr/bin/env python3
"""
修正後のサンドボックスサービステスト
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.sandbox_service import execute_python_code_sync


def test_error_handling():
    print("=== 修正後のエラーハンドリングテスト ===")

    # ZeroDivisionErrorのテスト
    print("1. ZeroDivisionError テスト:")
    result = execute_python_code_sync(
        'print("Before error"); x = 1 / 0; print("After error")'
    )
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  exit_code: {result.exit_code}")
    print(f"  error_type: {result.error_type}")
    print(f"  succeeded: {result.succeeded}")
    print()

    # 構文エラーのテスト
    print("2. SyntaxError テスト:")
    result = execute_python_code_sync('print("missing quote)')
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  exit_code: {result.exit_code}")
    print(f"  error_type: {result.error_type}")
    print(f"  succeeded: {result.succeeded}")
    print()

    # NameErrorのテスト
    print("3. NameError テスト:")
    result = execute_python_code_sync("print(undefined_variable)")
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  exit_code: {result.exit_code}")
    print(f"  error_type: {result.error_type}")
    print(f"  succeeded: {result.succeeded}")
    print()

    # 成功例のテスト
    print("4. 成功例のテスト:")
    result = execute_python_code_sync('print("Hello World!"); print(2 + 3)')
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  exit_code: {result.exit_code}")
    print(f"  error_type: {result.error_type}")
    print(f"  succeeded: {result.succeeded}")
    print()

    # stdin入力のテスト
    print("5. stdin入力のテスト:")
    result = execute_python_code_sync(
        'name = input("Enter your name: "); print(f"Hello, {name}!")',
        stdin_input="Bob\n",
    )
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  exit_code: {result.exit_code}")
    print(f"  error_type: {result.error_type}")
    print(f"  succeeded: {result.succeeded}")


if __name__ == "__main__":
    test_error_handling()
