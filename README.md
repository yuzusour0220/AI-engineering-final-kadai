# AI-engineering-final-kadai

## Docker環境構築

このプロジェクトはDocker Composeでフロントエンドとバックエンドのコンテナを管理します。

### 本番環境での起動方法

```bash
# Dockerイメージをビルドして起動
docker-compose up --build
```

フロントエンドは http://localhost:3000 でアクセス可能です。  
バックエンドは http://localhost:8000 でアクセス可能です。

### 開発環境での起動方法

開発環境では、ホットリロード機能が有効になっています。

```bash
# 開発用Dockerイメージをビルドして起動
docker-compose -f docker-compose.dev.yml up --build
```

### 各コンテナの役割

- **frontend**: Next.jsによるフロントエンドアプリケーション
- **backend**: FastAPIによるバックエンドAPI

### APIドキュメント

FastAPIの自動生成ドキュメントは以下のURLで確認できます：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
