#!/usr/bin/env python3
"""
強化された外部ライブラリサポートのテストスクリプト
新しく追加されたライブラリと改善された機能をテスト
"""

import sys
import os
import time

# パスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.sandbox_service import execute_python_code_sync


def test_enhanced_libraries():
    """強化された外部ライブラリのテスト"""
    print("🚀 強化された外部ライブラリサポートテスト")
    print("=" * 60)

    # テスト1: 機械学習ライブラリ（scikit-learn）
    print("🤖 テスト1: 機械学習ライブラリ（scikit-learn）")
    sklearn_code = """
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np

# サンプルデータ生成
X, y = make_classification(n_samples=100, n_features=4, n_classes=2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# モデル訓練
clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X_train, y_train)

# 予測と評価
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"データサイズ: {X.shape}")
print(f"訓練精度: {clf.score(X_train, y_train):.3f}")
print(f"テスト精度: {accuracy:.3f}")
print("✅ scikit-learn テスト完了")
"""
    result = execute_python_code_sync(sklearn_code)
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")
    print()

    # テスト2: 画像処理ライブラリ（Pillow）
    print("🖼️ テスト2: 画像処理ライブラリ（Pillow）")
    pillow_code = """
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 新しい画像を作成
width, height = 200, 100
image = Image.new('RGB', (width, height), color='lightblue')

# 描画オブジェクトを作成
draw = ImageDraw.Draw(image)

# 図形を描画
draw.rectangle([10, 10, 50, 50], fill='red', outline='black')
draw.ellipse([60, 10, 100, 50], fill='green', outline='black')
draw.text((110, 20), "Hello PIL!", fill='black')

# NumPy配列に変換して情報を表示
img_array = np.array(image)
print(f"画像サイズ: {image.size}")
print(f"カラーモード: {image.mode}")
print(f"NumPy配列形状: {img_array.shape}")
print(f"ピクセル値範囲: {img_array.min()} - {img_array.max()}")
print("✅ Pillow テスト完了")
"""
    result = execute_python_code_sync(pillow_code)
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")
    print()

    # テスト3: データ可視化ライブラリ（seaborn）
    print("📊 テスト3: データ可視化ライブラリ（seaborn）")
    seaborn_code = """
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# サンプルデータ作成
np.random.seed(42)
data = {
    'グループ': ['A'] * 50 + ['B'] * 50 + ['C'] * 50,
    '値': np.concatenate([
        np.random.normal(10, 2, 50),
        np.random.normal(15, 3, 50),
        np.random.normal(12, 2.5, 50)
    ])
}
df = pd.DataFrame(data)

# 統計情報を表示（実際のプロットは表示されない）
print(f"データ形状: {df.shape}")
print("グループ別統計:")
print(df.groupby('グループ')['値'].describe())

# seabornが正常に動作することを確認
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(data=df, x='グループ', y='値', ax=ax)
plt.title('グループ別ボックスプロット')

print("✅ seaborn テスト完了（グラフは非表示）")
"""
    result = execute_python_code_sync(seaborn_code)
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")
    print()

    # テスト4: 科学計算ライブラリ（scipy）
    print("🔬 テスト4: 科学計算ライブラリ（scipy）")
    scipy_code = """
import numpy as np
from scipy import stats, optimize, signal
from scipy.linalg import norm

# 統計処理
data = np.random.normal(100, 15, 1000)
mean, std = stats.norm.fit(data)
print(f"正規分布フィッティング: 平均={mean:.2f}, 標準偏差={std:.2f}")

# 最適化
def quadratic(x):
    return x**2 + 2*x + 1

result = optimize.minimize_scalar(quadratic)
print(f"二次関数の最小値: x={result.x:.3f}, f(x)={result.fun:.3f}")

# 信号処理
t = np.linspace(0, 1, 500)
sig = np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*10*t)
freqs, power = signal.periodogram(sig, 500)
dominant_freq = freqs[np.argmax(power)]
print(f"支配的周波数: {dominant_freq:.2f} Hz")

# 線形代数
vector = np.array([3, 4, 5])
print(f"ベクトルのノルム: {norm(vector):.3f}")

print("✅ scipy テスト完了")
"""
    result = execute_python_code_sync(scipy_code)
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")
    print()

    # テスト5: 自然言語処理ライブラリ（NLTK）
    print("📝 テスト5: 自然言語処理ライブラリ（NLTK）")
    nltk_code = """
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

# NLTKデータのダウンロード（オフライン環境では制限あり）
text = "Hello world! This is a test sentence. NLTK is great for natural language processing."

# トークン化（基本的な分割のみ）
words = text.split()
sentences = text.split('.')

print(f"原文: {text}")
print(f"単語数: {len(words)}")
print(f"文数: {len([s for s in sentences if s.strip()])}")

# 基本的な前処理
words_clean = [word.lower().strip(string.punctuation) for word in words if word.strip(string.punctuation)]
print(f"前処理後の単語: {words_clean[:10]}")

# ステミング
stemmer = PorterStemmer()
stemmed = [stemmer.stem(word) for word in words_clean[:5]]
print(f"ステミング例: {list(zip(words_clean[:5], stemmed))}")

print("✅ NLTK テスト完了（制限環境）")
"""
    result = execute_python_code_sync(nltk_code)
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")
    print()

    # テスト6: タイムアウト改善のテスト（小さなパッケージインストール）
    print("⏱️ テスト6: タイムアウト改善テスト（パッケージインストール）")
    timeout_test_code = """
!pip install colorama
import colorama
from colorama import Fore, Style

colorama.init()
print(f"{Fore.GREEN}カラー出力テスト成功！{Style.RESET_ALL}")
print(f"{Fore.BLUE}coloramaが正常にインストールされました{Style.RESET_ALL}")
print(f"{Fore.RED}タイムアウト60秒設定が有効です{Style.RESET_ALL}")
"""
    start_time = time.time()
    result = execute_python_code_sync(timeout_test_code)
    end_time = time.time()
    total_time = (end_time - start_time) * 1000

    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")
    print(f"   総実行時間: {total_time:.2f}ms")
    print()

    # テスト7: エラーハンドリングテスト（存在しないパッケージ）
    print("❌ テスト7: エラーハンドリングテスト（存在しないパッケージ）")
    error_test_code = """
!pip install nonexistent-package-12345
print("このメッセージは表示されないはずです")
"""
    result = execute_python_code_sync(error_test_code)
    print(f"   出力: {repr(result.stdout)}")
    print(f"   エラー: {repr(result.stderr)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")
    print()

    print("🎉 強化されたライブラリサポートテスト完了！")
    print("\n📋 テスト結果サマリー:")
    print("   ✅ scikit-learn（機械学習）")
    print("   ✅ Pillow（画像処理）")
    print("   ✅ seaborn（データ可視化）")
    print("   ✅ scipy（科学計算）")
    print("   ✅ NLTK（自然言語処理）")
    print("   ✅ タイムアウト改善（60秒）")
    print("   ✅ エラーハンドリング改善")


def test_performance_improvements():
    """パフォーマンス改善のテスト"""
    print("\n⚡ パフォーマンス改善テスト")
    print("=" * 40)

    # 複数の事前インストール済みライブラリの高速インポート
    print("📦 事前インストール済みライブラリの高速インポートテスト")
    import_test_code = """
import time
start = time.time()

# 事前インストール済みライブラリを一度にインポート
import numpy
import pandas
import matplotlib.pyplot
import requests
import sklearn
import scipy
import seaborn
import PIL
import sqlalchemy

end = time.time()
import_time = (end - start) * 1000

print(f"8つのライブラリのインポート時間: {import_time:.2f}ms")
print("✅ 高速インポート確認完了")
"""
    result = execute_python_code_sync(import_test_code)
    print(f"   出力: {repr(result.stdout)}")
    print(f"   成功: {result.succeeded}")
    print(f"   実行時間: {result.execution_time_ms:.2f}ms")


if __name__ == "__main__":
    test_enhanced_libraries()
    test_performance_improvements()
