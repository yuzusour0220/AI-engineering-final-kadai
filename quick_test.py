#!/usr/bin/env python3
import os
import sys

# バックエンドのパスを追加
backend_path = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, backend_path)

print("Testing stderr variable fix...")
print("=" * 50)

try:
    # インポートテスト
    from services.sandbox_service import execute_python_code_sync

    print("✓ Import successful")

    # 簡単なコードテスト
    simple_code = "print('Hello, World!')"
    result = execute_python_code_sync(simple_code)
    print(f"✓ Simple code execution: {result.succeeded}")
    print(f"  Output: {result.stdout.strip()}")

    # エラーコードテスト
    error_code = "undefined_variable_test"
    result = execute_python_code_sync(error_code)
    print(f"✓ Error code execution completed (exit_code: {result.exit_code})")
    print(f"  Has stderr: {'Yes' if result.stderr else 'No'}")

    if result.stderr:
        print(f"  Stderr preview: {result.stderr[:100]}...")

    print("\n" + "=" * 50)
    print("✓ All tests completed successfully!")
    print("✓ No 'stderr not defined' error occurred!")

except Exception as e:
    print(f"✗ Error occurred: {e}")
    import traceback

    traceback.print_exc()
