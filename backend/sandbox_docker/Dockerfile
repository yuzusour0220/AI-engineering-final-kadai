# サンドボックス実行用のDockerfile
# プロジェクトで使用されているPython 3.13-slimをベースイメージとして使用
FROM python:3.13-slim

# システムの更新とセキュリティパッケージのインストール
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 必要なPythonライブラリがあればここでインストール
# 現在は最小限の構成のため、追加ライブラリはなし
# RUN pip install --no-cache-dir some-library

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
