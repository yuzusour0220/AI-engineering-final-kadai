#!/bin/sh
# wait-for-it.sh - バックエンドサーバーの起動を待つスクリプト

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

echo "バックエンドサーバー ${host}:${port} の起動を待機しています..."

# サーバー起動を待機
until nc -z $host $port; do
  echo "バックエンドはまだ利用できません - 待機中..."
  sleep 1
done

echo "バックエンドサーバーが起動しました - 処理を続行します"
exec $cmd
