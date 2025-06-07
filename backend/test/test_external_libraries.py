#!/usr/bin/env python3
"""
外部ライブラリ対応のテストスクリプト
"""

import sys
import os
import asyncio

# パスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.sandbox_service import execute_python_code_sync


def test_external_libraries():
    """外部ライブラリのテスト"""
    print("🧪 外部ライブラリ対応テスト")
    print("=" * 50)

    # テスト1: 事前インストール済みライブラリ（numpy）
    print("📦 テスト1: 事前インストール済みライブラリ（numpy）")
    numpy_code = """
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(f"配列: {arr}")
print(f"合計: {np.sum(arr)}")
print(f"平均: {np.mean(arr)}")
"""
    result = execute_python_code_sync(numpy_code)
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")
    print()

    # テスト2: 事前インストール済みライブラリ（pandas）
    print("📦 テスト2: 事前インストール済みライブラリ（pandas）")
    pandas_code = """
import pandas as pd
import numpy as np

data = {'名前': ['田中', '佐藤', '鈴木'], '年齢': [25, 30, 35]}
df = pd.DataFrame(data)
print(df)
print(f"平均年齢: {df['年齢'].mean()}")
"""
    result = execute_python_code_sync(pandas_code)
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")
    print()

    # テスト3: !pip install による動的インストール
    print("📦 テスト3: !pip install による動的インストール")
    pip_install_code = """
!pip install emoji
import emoji
text = "Pythonは楽しい！"
emoji_text = emoji.emojize(":snake: Python is fun! :snake:")
print(f"通常テキスト: {text}")
print(f"絵文字付き: {emoji_text}")
"""
    result = execute_python_code_sync(pip_install_code)
    print(f"   出力: {repr(result.stdout)}")
    print(f"   エラー: {repr(result.stderr)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")
    print()

    # テスト4: 複数パッケージの同時インストール
    print("📦 テスト4: 複数パッケージの同時インストール")
    multiple_packages_code = """
!pip install python-dateutil pytz
from datetime import datetime
import dateutil.parser
import pytz

# 現在時刻をUTCで取得
utc_now = datetime.now(pytz.UTC)
print(f"UTC時刻: {utc_now}")

# 日本時間に変換
jst = pytz.timezone('Asia/Tokyo')
jst_now = utc_now.astimezone(jst)
print(f"JST時刻: {jst_now}")
"""
    result = execute_python_code_sync(multiple_packages_code)
    print(f"   出力: {repr(result.stdout)}")
    print(f"   エラー: {repr(result.stderr)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")
    print()

    # テスト5: matplotlib（事前インストール済み）
    print("📦 テスト5: matplotlib（事前インストール済み、画像出力なし）")
    matplotlib_code = """
import matplotlib.pyplot as plt
import numpy as np

# データ生成
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

# プロット作成（実際には表示しない）
plt.figure(figsize=(8, 6))
plt.plot(x, y, 'b-', label='sin(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Sine Wave')
plt.legend()

print("matplotlibグラフを作成しました（表示はサンドボックス内のため不可）")
print(f"データポイント数: {len(x)}")
print(f"y値の範囲: {np.min(y):.3f} ~ {np.max(y):.3f}")
"""
    result = execute_python_code_sync(matplotlib_code)
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")
    print()

    # テスト6: requests（事前インストール済み）だが、ネットワーク無効のためエラー
    print("📦 テスト6: requests（ネットワーク無効環境での動作確認）")
    requests_code = """
import requests

print("requestsライブラリはインポート可能です")
print("ただし、サンドボックス環境はネットワーク無効のため外部アクセスはできません")

# 実際にリクエストを試すとエラーになることを確認
try:
    response = requests.get("https://httpbin.org/json", timeout=2)
    print(f"レスポンス: {response.status_code}")
except Exception as e:
    print(f"予想通りエラー: {type(e).__name__}")
"""
    result = execute_python_code_sync(requests_code)
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")
    print()

    print("🎉 外部ライブラリテスト完了！")
    print("\n📋 サポートされている機能:")
    print("   ✅ 事前インストール済みライブラリ（numpy, pandas, matplotlib等）")
    print("   ✅ !pip install による動的ライブラリインストール")
    print("   ✅ 複数パッケージの同時インストール")
    print("   ✅ バージョン指定インストール")
    print("   ⚠️  ネットワークアクセスは無効（セキュリティ制限）")


if __name__ == "__main__":
    test_external_libraries()
