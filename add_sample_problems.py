#!/usr/bin/env python3
"""
サンプル問題を追加するスクリプト
"""

import requests
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

# サンプル問題データ
sample_problems = [
    {
        "id": 1,
        "title": "Hello World",
        "description": """基本的なPythonプログラムを作成してください。

要求:
- "Hello, World!" という文字列を出力するプログラムを作成してください
- print関数を使用してください

例:
出力: Hello, World!""",
        "correct_code": 'print("Hello, World!")',
    },
    {
        "id": 2,
        "title": "数値の計算",
        "description": """2つの数値を受け取り、その合計を出力するプログラムを作成してください。

要求:
- 変数 a = 10, b = 20 を定義してください
- これらの数値の合計を計算し、結果を出力してください

例:
出力: 30""",
        "correct_code": """a = 10
b = 20
result = a + b
print(result)""",
    },
]


def add_sample_problems():
    """サンプル問題をAPIに追加"""
    for problem in sample_problems:
        try:
            response = requests.post(
                f"{API_BASE_URL}/problems/",
                json=problem,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                print(f"✅ 問題 {problem['id']} '{problem['title']}' を追加しました")
            elif response.status_code == 400:
                print(f"⚠️  問題 {problem['id']} は既に存在します")
            else:
                print(f"❌ 問題 {problem['id']} の追加に失敗: {response.status_code}")
                print(f"   レスポンス: {response.text}")

        except requests.RequestException as e:
            print(f"❌ API接続エラー: {e}")
            print("   バックエンドサーバーが起動していることを確認してください")
            break


if __name__ == "__main__":
    print("サンプル問題を追加しています...")
    add_sample_problems()
    print("完了！")
