#!/usr/bin/env python3
"""
サンドボックスサービスの完全なテストスクリプト
"""

import sys
import os
import asyncio

# パスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.sandbox_service import (
    execute_python_code_sync,
    execute_python_code_in_docker,
    CodeExecutionResult,
)


def test_sync_functionality():
    """同期版のテスト"""
    print("=== 同期版サンドボックスサービステスト ===")

    # テスト1: 基本的なHello Worldテスト
    print("テスト1: 基本的なHello World")
    test_code = 'print("Hello, World!")'

    result = execute_python_code_sync(test_code)
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  exit_code: {result.exit_code}")
    print(f"  succeeded: {result.succeeded}")
    print(f"  execution_time_ms: {result.execution_time_ms:.2f}")
    print()

    # テスト2: 計算のテスト
    print("テスト2: 計算コード")
    calc_code = """
x = 10
y = 20
result = x + y
print(f"x + y = {result}")
"""

    result = execute_python_code_sync(calc_code)
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  succeeded: {result.succeeded}")
    print()

    # テスト3: エラーを含むコード
    print("テスト3: 実行時エラー (ZeroDivisionError)")
    error_code = """
print("計算開始")
x = 1 / 0
print("計算終了")
"""

    result = execute_python_code_sync(error_code)
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  exit_code: {result.exit_code}")
    print(f"  error_type: {result.error_type}")
    print(f"  succeeded: {result.succeeded}")
    print()

    # テスト4: 構文エラー
    print("テスト4: 構文エラー")
    syntax_error_code = """
print("This has a syntax error"
# 括弧が閉じていない
"""

    result = execute_python_code_sync(syntax_error_code)
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  exit_code: {result.exit_code}")
    print(f"  error_type: {result.error_type}")
    print(f"  succeeded: {result.succeeded}")
    print()

    # テスト5: stdin入力のテスト
    print("テスト5: stdin入力")
    stdin_code = """
name = input("Enter your name: ")
print(f"Hello, {name}!")
"""

    result = execute_python_code_sync(stdin_code, stdin_input="Alice\n")
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  exit_code: {result.exit_code}")
    print(f"  succeeded: {result.succeeded}")
    print()


async def test_async_functionality():
    """非同期版のテスト"""
    print("=== 非同期版サンドボックスサービステスト ===")

    # テスト1: 基本的なHello Worldテスト
    print("テスト1: 基本的なHello World (Async)")
    test_code = 'print("Hello from async!")'

    result = await execute_python_code_in_docker(test_code)
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  exit_code: {result.exit_code}")
    print(f"  succeeded: {result.succeeded}")
    print(f"  execution_time_ms: {result.execution_time_ms:.2f}")
    print()

    # テスト2: 複雑な計算
    print("テスト2: 複雑な計算 (Async)")
    complex_code = """
import math

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
print(f"5! = {result}")
print(f"π = {math.pi:.4f}")
"""

    result = await execute_python_code_in_docker(complex_code)
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  succeeded: {result.succeeded}")
    print()

    # テスト3: NameError
    print("テスト3: NameError (Async)")
    name_error_code = """
print("Before error")
print(undefined_variable)
print("After error")
"""

    result = await execute_python_code_in_docker(name_error_code)
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  error_type: {result.error_type}")
    print(f"  succeeded: {result.succeeded}")
    print()


def test_edge_cases():
    """エッジケースのテスト"""
    print("=== エッジケーステスト ===")

    # テスト1: 空のコード
    print("テスト1: 空のコード")
    result = execute_python_code_sync("")
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  succeeded: {result.succeeded}")
    print()

    # テスト2: 複数行の複雑なコード
    print("テスト2: 複数行の複雑なコード")
    complex_code = """
class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def get_history(self):
        return self.history

calc = Calculator()
result1 = calc.add(5, 3)
result2 = calc.add(10, 7)

print(f"結果1: {result1}")
print(f"結果2: {result2}")
print("履歴:")
for entry in calc.get_history():
    print(f"  {entry}")
"""

    result = execute_python_code_sync(complex_code)
    print(f"  stdout: {repr(result.stdout)}")
    print(f"  stderr: {repr(result.stderr)}")
    print(f"  succeeded: {result.succeeded}")
    print()


def main():
    """メイン関数"""
    print("サンドボックスサービスの総合テストを開始します\n")

    try:
        # 同期版テスト
        test_sync_functionality()

        print("\n" + "=" * 60 + "\n")

        # 非同期版テスト
        asyncio.run(test_async_functionality())

        print("\n" + "=" * 60 + "\n")

        # エッジケーステスト
        test_edge_cases()

        print("\n✅ すべてのテストが完了しました！")

    except Exception as e:
        print(f"\n❌ テスト中にエラーが発生しました: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
