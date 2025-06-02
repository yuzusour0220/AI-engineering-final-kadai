FROM python:3.13-slim

WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y netcat-openbsd && \
    pip install requests==2.32.3 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# スクリプトをコピー
COPY add_sample_problems.py .
COPY data-init/wait-for-it.sh .

# 実行権限を付与とスクリプトの改行コードを修正
RUN chmod +x add_sample_problems.py && \
    chmod +x wait-for-it.sh && \
    sed -i 's/\r$//' wait-for-it.sh

# バックエンドサーバーの起動を待ってから実行
CMD ["sh", "wait-for-it.sh", "backend", "8000", "python", "add_sample_problems.py"]
