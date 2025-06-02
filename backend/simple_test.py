#!/usr/bin/env python3
"""
最も基本的なサンドボックステスト
"""

import sys
import os

# パスを追加
sys.path.append(
    "/Users/takumisakai/自主勉/AIエンジニアリング/AI-engineering-final-kadai/backend"
)

print("=== 基本テスト開始 ===")

try:
    print("1. サービスのインポート...")
    from services.sandbox_service import execute_python_code_sync

    print("   ✓ インポート成功")

    print("2. 簡単なコード実行...")
    result = execute_python_code_sync('print("test")')
    print(f"   結果: {result}")

except Exception as e:
    print(f"   ❌ エラー: {e}")
    import traceback

    traceback.print_exc()

print("=== テスト完了 ===")
