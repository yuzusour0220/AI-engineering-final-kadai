# サンドボックス実行用のDockerfile
# プロジェクトで使用されているPython 3.13-slimをベースイメージとして使用
FROM python:3.13-slim

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
