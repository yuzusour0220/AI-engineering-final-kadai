# サンドボックス実行用のDockerfile
# プロジェクトで使用されているPython 3.13-slimをベースイメージとして使用
FROM python:3.13-slim

# # システムの更新とセキュリティパッケージのインストール
# # 科学計算ライブラリのビルドに必要なツールを追加
# RUN apt-get update && apt-get install -y \
#     --no-install-recommends \
#     build-essential \
#     gcc \
#     g++ \
#     gfortran \
#     libopenblas-dev \
#     liblapack-dev \
#     && rm -rf /var/lib/apt/lists/*

# よく使用される科学計算・データ分析ライブラリを事前インストール
# これにより、実行時のインストール時間を短縮し、よくあるライブラリは確実に利用可能になる
# 軽量なライブラリから順にインストールし、重いライブラリは事前ビルド版を使用
# RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
#     pip install --no-cache-dir \
#     "requests>=2.31.0,<3.0.0" \
#     "python-dateutil>=2.8.0,<3.0.0" \
#     "pytz>=2023.3" \
#     "tqdm>=4.65.0,<5.0.0" \
#     "beautifulsoup4>=4.12.0,<5.0.0" && \
#     pip install --no-cache-dir \
#     "numpy>=1.24.0,<2.0.0" && \
#     pip install --no-cache-dir \
#     "pandas>=2.0.0,<3.0.0" \
#     "matplotlib>=3.7.0,<4.0.0" \
#     "seaborn>=0.12.0,<1.0.0" \
#     "pillow>=10.0.0,<11.0.0" && \
#     pip install --no-cache-dir \
#     "scipy>=1.11.0,<2.0.0" \
#     "scikit-learn>=1.3.0,<2.0.0"

# セキュリティのため非rootユーザーを作成
RUN useradd -ms /bin/bash sandbox_user

# ユーザーを切り替え
USER sandbox_user

# 作業ディレクトリを設定
WORKDIR /app

# コンテナ起動時に実行されるデフォルトコマンド
# 実際のスクリプトはFastAPI側から動的にマウントされるため、
# ここでは無限待機のコマンドを設定（実際にはdocker runで上書きされる）
CMD ["sleep", "infinity"]
