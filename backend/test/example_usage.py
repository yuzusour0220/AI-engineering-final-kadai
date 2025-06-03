"""
サンドボックスサービスの使用例
"""

import asyncio
from services.sandbox_service import (
    execute_python_code_sync,
    execute_python_code_in_docker,
)


def basic_example():
    """基本的な使用例"""
    print("=== 基本的なコード実行 ===")

    # Hello World
    result = execute_python_code_sync('print("Hello, World!")')
    print(f"出力: {result.stdout}")
    print(f"成功: {result.succeeded}")
    print(f"実行時間: {result.execution_time_ms}ms")
    print()


def calculation_example():
    """計算の例"""
    print("=== 計算の実行 ===")

    code = """
x = 10
y = 20
result = x + y
print(f"{x} + {y} = {result}")

# リストの操作
numbers = [1, 2, 3, 4, 5]
squares = [n**2 for n in numbers]
print(f"squares: {squares}")
"""

    result = execute_python_code_sync(code)
    print(f"出力:\n{result.stdout}")
    print(f"実行時間: {result.execution_time_ms}ms")
    print()


def input_example():
    """標準入力を使う例"""
    print("=== 標準入力付きの実行 ===")

    code = """
name = input("お名前を入力してください: ")
age = int(input("年齢を入力してください: "))
print(f"こんにちは、{name}さん！")
print(f"あなたは{age}歳ですね。")
"""

    # stdin_inputで入力データを渡す
    stdin_data = "田中太郎\n25\n"
    result = execute_python_code_sync(code, stdin_input=stdin_data)
    print(f"出力:\n{result.stdout}")
    print()


def error_handling_example():
    """エラーハンドリングの例"""
    print("=== エラーハンドリング ===")

    # ゼロ除算エラー
    result = execute_python_code_sync("x = 1 / 0")
    print(f"エラータイプ: {result.error_type}")
    print(f"エラー内容: {result.stderr}")
    print(f"成功: {result.succeeded}")
    print()

    # 構文エラー
    result = execute_python_code_sync('print("Hello World"')  # 閉じ括弧なし
    print(f"エラータイプ: {result.error_type}")
    print(f"成功: {result.succeeded}")
    print()


async def async_example():
    """非同期実行の例"""
    print("=== 非同期実行 ===")

    code = """
import time
print("非同期処理開始")
time.sleep(1)  # 1秒待機
print("非同期処理完了")
"""

    result = await execute_python_code_in_docker(code)
    print(f"出力:\n{result.stdout}")
    print(f"実行時間: {result.execution_time_ms}ms")
    print()


def complex_example():
    """複雑なコードの例"""
    print("=== 複雑なコード実行 ===")

    code = """
# フィボナッチ数列を計算
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 最初の10個のフィボナッチ数を計算
fib_numbers = [fibonacci(i) for i in range(10)]
print(f"フィボナッチ数列: {fib_numbers}")

# 辞書を使ったデータ処理
students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78}
]

# 平均点を計算
average = sum(student["score"] for student in students) / len(students)
print(f"平均点: {average:.1f}")

# 90点以上の学生を抽出
high_scorers = [s["name"] for s in students if s["score"] >= 90]
print(f"90点以上: {high_scorers}")
"""

    result = execute_python_code_sync(code)
    print(f"出力:\n{result.stdout}")
    print(f"実行時間: {result.execution_time_ms}ms")
    print()


if __name__ == "__main__":
    print("🚀 サンドボックスサービス使用例\n")

    # 同期実行の例
    basic_example()
    calculation_example()
    input_example()
    error_handling_example()
    complex_example()

    # 非同期実行の例
    asyncio.run(async_example())

    print("✅ 全ての例が完了しました！")
