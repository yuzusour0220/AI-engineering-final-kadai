#!/usr/bin/env python3

import sys
import os

# パスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 簡単なインポートテスト
try:
    from services.sandbox_service import execute_python_code_sync, CodeExecutionResult

    print("✅ インポート成功")

    # 基本的なテスト
    print("🧪 基本的な Hello World テスト")
    result = execute_python_code_sync('print("Hello, Docker!")')

    print(f"stdout: {repr(result.stdout)}")
    print(f"stderr: {repr(result.stderr)}")
    print(f"exit_code: {result.exit_code}")
    print(f"succeeded: {result.succeeded}")
    print(f"execution_time_ms: {result.execution_time_ms:.2f}")

    if result.succeeded:
        print("✅ 基本テスト成功！")
    else:
        print("❌ 基本テスト失敗")

except ImportError as e:
    print(f"❌ インポートエラー: {e}")

    # ファイルの存在確認
    sandbox_file = "services/sandbox_service.py"
    if os.path.exists(sandbox_file):
        print(f"📁 ファイルは存在します: {sandbox_file}")
        with open(sandbox_file, "r") as f:
            content = f.read()
            print(f"📏 ファイルサイズ: {len(content)} 文字")
            print(f"🔍 最初の200文字:")
            print(content[:200])
    else:
        print(f"📁 ファイルが存在しません: {sandbox_file}")

except Exception as e:
    print(f"❌ その他のエラー: {e}")
    import traceback

    traceback.print_exc()
