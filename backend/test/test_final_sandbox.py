#!/usr/bin/env python3
"""
最終的なサンドボックスサービスの確認テスト
"""

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.sandbox_service import (
    execute_python_code_sync,
    execute_python_code_in_docker,
)


def test_final():
    print("🧪 サンドボックスサービスの最終確認テスト")
    print("=" * 50)

    # 1. 基本的な実行テスト
    print("✅ 基本的な実行テスト")
    result = execute_python_code_sync('print("Hello, Sandbox!")')
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print()

    # 2. エラーハンドリングテスト
    print("✅ エラーハンドリングテスト")
    result = execute_python_code_sync("x = 1 / 0")
    print(f"   エラータイプ: {result.error_type}")
    print(f"   終了コード: {result.exit_code}")
    print()

    # 3. stdin入力テスト
    print("✅ stdin入力テスト")
    result = execute_python_code_sync(
        'name = input("Name: "); print(f"Hi, {name}!")', stdin_input="Python\n"
    )
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print()

    # 4. 複雑な計算テスト
    print("✅ 複雑な計算テスト")
    result = execute_python_code_sync("""
import math

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(f"fibonacci(10) = {result}")
print(f"sqrt(144) = {math.sqrt(144)}")
""")
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print()


async def test_async_final():
    print("🚀 非同期版テスト")
    print("=" * 50)

    result = await execute_python_code_in_docker('print("Async works!")')
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print()


if __name__ == "__main__":
    test_final()

    print("🚀 非同期版もテスト中...")
    asyncio.run(test_async_final())

    print("🎉 すべてのテストが完了しました！")
    print("\n📋 サンドボックスサービスの機能:")
    print("   - Pythonコードの安全な実行")
    print("   - Docker コンテナでの分離実行")
    print("   - セキュリティ制限 (ネットワーク無効, メモリ制限)")
    print("   - エラーハンドリング (構文エラー、実行時エラー)")
    print("   - stdin入力サポート")
    print("   - 実行時間制限 (5秒)")
    print("   - 同期・非同期両方の実行モード")
