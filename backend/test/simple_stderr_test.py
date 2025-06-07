#!/usr/bin/env python3
"""
シンプルなstderr修正テスト
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

try:
    from services.sandbox_service import execute_python_code_sync

    # エラーが発生するコードでテスト
    error_code = """
print("Testing stderr fix")
this_is_undefined_variable
"""

    print("Testing stderr variable fix...")
    result = execute_python_code_sync(error_code)

    print(f"Exit code: {result.exit_code}")
    print(f"Error type: {result.error_type}")
    print(f"Stderr length: {len(result.stderr) if result.stderr else 0}")
    print(f"Has stderr: {'Yes' if result.stderr else 'No'}")

    if result.stderr:
        print("Stderr content (first 200 chars):")
        print(result.stderr[:200])

    print("Test completed successfully - no 'stderr not defined' error!")

except Exception as e:
    print(f"Error during test: {e}")
    import traceback

    traceback.print_exc()
