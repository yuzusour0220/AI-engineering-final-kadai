#!/usr/bin/env python3
"""
サンドボックスサービスのテストスクリプト
"""

import asyncio
import sys
import os

# サンドボックスサービスをインポート
sys.path.append(os.path.dirname(__file__))
from services.sandbox_service import execute_python_code_in_docker, test_sandbox


async def main():
    print("=== Starting Sandbox Service Test ===")

    try:
        # 基本的なテスト
        print("Testing basic Python code execution...")
        result = await execute_python_code_in_docker('print("Hello from sandbox!")')
        print(f"Result: {result}")
        print()

        # 完全なテスト実行
        print("Running comprehensive tests...")
        await test_sandbox()

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
