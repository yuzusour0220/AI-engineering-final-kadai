# サンドボックスDockerfile

このディレクトリには、コード実行用のサンドボックス環境を構築するためのDockerfileが含まれています。

## 概要

このDockerfileは、ユーザーから送信されたPythonコードを安全に実行するためのサンドボックス環境を提供します。

## 特徴

- **ベースイメージ**: `python:3.13-slim` (プロジェクトのメインバージョンと一致)
- **セキュリティ**: 非rootユーザー (`sandbox_user`) での実行
- **軽量**: 最小限の依存関係
- **分離**: ネットワーク無効化とメモリ制限による安全な実行環境

## ビルド方法

```bash
cd backend/sandbox_docker
docker build -t python-sandbox .
```

## 使用方法

このイメージは`services/sandbox_service.py`によって自動的に使用されます。
手動でテストする場合：

```bash
# 基本的なテスト
echo 'print("Hello, Sandbox!")' | docker run --rm -i python-sandbox python

# ユーザー確認
docker run --rm python-sandbox whoami
# -> sandbox_user

# Pythonバージョン確認
docker run --rm python-sandbox python --version
# -> Python 3.13.3
```

## セキュリティ機能

1. **非rootユーザー**: `sandbox_user`として実行
2. **ネットワーク分離**: `network_disabled=True`
3. **メモリ制限**: 128MBの制限
4. **一時実行**: `remove=True`でコンテナ自動削除
5. **タイムアウト**: 5秒での実行制限

## 統合

- `services/sandbox_service.py`で使用
- `routers/submissions.py`のコード実行エンドポイントで利用
- FastAPIアプリケーションから自動呼び出し

## 注意事項

- Docker Desktopまたはdockerデーモンが実行中である必要があります
- 初回ビルド後は、コードの変更があった場合のみ再ビルドが必要です
- 本番環境では追加のセキュリティ設定を検討してください
