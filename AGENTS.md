# AIエンジニアリング課題システム - エージェントガイド

## 📋 プロジェクト概要

このプロジェクトは、学習者がPythonプログラミング課題に取り組み、コードを提出すると、AIがコード分析してアドバイスを提供するWebアプリケーションです。

### 🛠 技術スタック

**フロントエンド**
- Next.js 15 (App Router)
- React 18 + TypeScript
- Tailwind CSS
- Monaco Editor

**バックエンド**
- FastAPI
- SQLAlchemy + SQLite
- Pydantic
- Docker サンドボックス（コード実行）
- Hugging Face API（AIアドバイス生成）

**インフラ**
- Docker & Docker Compose
- CI/CD (GitHub Actions)

## 📁 プロジェクト構造

```
AI-engineering-final-kadai/
├── frontend/                    # Next.js フロントエンド
│   ├── src/
│   │   ├── app/                # App Router ページ
│   │   ├── components/         # React コンポーネント
│   │   ├── lib/               # ユーティリティ・API クライアント
│   │   └── types/             # TypeScript 型定義
├── backend/                     # FastAPI バックエンド
│   ├── routers/               # API エンドポイント
│   ├── services/              # ビジネスロジック
│   │   ├── sandbox_service.py # Dockerサンドボックス
│   │   └── advice_service.py  # AI アドバイス生成
│   ├── models.py              # Pydantic モデル
│   ├── database.py            # SQLAlchemy 設定
│   ├── sandbox_docker/        # サンドボックス用Dockerfile
│   └── test/                  # テストファイル
├── docker-compose.yml          # 本番用
├── docker-compose.dev.yml      # 開発用
└── .github/workflows/ci.yml    # CI/CD
```

## 🚀 開発環境セットアップ

### 初期セットアップ
```bash
# リポジトリクローン後
docker-compose up --build

# アクセス先
# フロントエンド: http://localhost:3000
# バックエンドAPI: http://localhost:8000/docs
```

### 開発モード
```bash
# ホットリロード有効
docker-compose -f docker-compose.dev.yml up --build
```

### サンドボックスイメージのビルド
```bash
cd backend/sandbox_docker
docker build -t python-sandbox .
```

## 💻 開発ガイドライン

### フロントエンド開発

**ファイル配置**
- `src/app/` - Next.js App Routerページ
- `src/components/` - 再利用可能コンポーネント  
- `src/lib/api.ts` - バックエンドAPI呼び出し
- `src/types/api.ts` - API型定義（バックエンドのPydanticモデルと一致）

**コンポーネント作成**
- TypeScript必須
- Tailwind CSSでスタイリング
- 状態管理は`useState`/`useEffect`
- エラーハンドリング必須

**API呼び出し**
```typescript
// lib/api.ts を使用
import { apiClient } from '@/lib/api';
const problems = await apiClient.getProblems();
```

### バックエンド開発

**API設計**
- FastAPIのauto-generated docsを活用 (`/docs`)
- Pydanticモデルで型安全性確保
- 適切なHTTPステータスコード使用

**新規エンドポイント追加**
1. `models.py` でPydanticモデル定義
2. `routers/` に新しいルーター作成
3. `main.py` でルーター登録
4. フロントエンドの型定義更新

**サンドボックス使用**
```python
from services.sandbox_service import execute_python_code_sync

result = execute_python_code_sync(user_code)
if result.succeeded:
    print(f"出力: {result.stdout}")
else:
    print(f"エラー: {result.stderr}")
```

## 🧪 テスト実行

### バックエンドテスト
```bash
# 基本的なサンドボックステスト
python backend/test/simple_sandbox_test.py

# 完全なサンドボックステスト  
python backend/test/test_sandbox_complete.py

# API統合テスト
python backend/test/api_smoke_test.py

# Docker基本テスト
python backend/test/test_docker_basic.py
```

### CI/CD
```bash
# GitHub Actions で自動実行される内容
pip install -r backend/requirements.txt
docker build -t python-sandbox backend/sandbox_docker
python backend/test/test_docker_basic.py
docker compose up -d backend
python backend/test/api_smoke_test.py
```

## 🔧 主要サービス

### サンドボックスサービス (`services/sandbox_service.py`)

**機能**
- Dockerコンテナでの安全なPythonコード実行
- セキュリティ制限（ネットワーク無効、メモリ128MB、5秒タイムアウト）
- エラー詳細検出（構文エラー、実行時エラー）
- 標準入力サポート
- Jupyterノートブック対応

**使用例**
```python
# 同期実行
result = execute_python_code_sync('print("Hello")')

# 非同期実行  
result = await execute_python_code_in_docker('print("Hello")')
```

### AIアドバイスサービス (`services/advice_service.py`)

**機能**
- Hugging Face API経由でのAIアドバイス生成
- 学習者のコード、実行結果、エラー内容を分析
- 教育的なフィードバック提供

**設定要件**
```bash
# 環境変数設定
HUGGINGFACE_API_KEY=your_api_key
```

## 🛠 よくある作業

### 新しい問題の追加
1. データベースに問題データ追加（SQLiteファイル直接編集）
2. フロントエンドの問題一覧更新が必要（現在ハードコード）

### エラーデバッグ

**Dockerエラー**
```bash
# Dockerデーモン確認
docker --version
docker ps

# サンドボックスイメージ確認
docker images | grep python-sandbox
```

**APIエラー**
- FastAPI docs (`http://localhost:8000/docs`) でエンドポイント確認
- バックエンドログ確認 (`docker-compose logs backend`)

**フロントエンドエラー**  
- ブラウザ開発者ツールでコンソールエラー確認
- Next.jsサーバーログ確認 (`docker-compose logs frontend`)

## 📝 コードスタイル

### TypeScript/React
- ESLint設定に従う (`npm run lint`)
- コンポーネントはPascalCase
- ファイル名はkebab-case

### Python
- FastAPI conventions
- type hints必須
- docstring推奨

## 🚧 既知の制限事項

1. **固定問題リスト**: ホームページの問題一覧がハードコード
2. **SQLiteファイル**: Docker再起動時のデータ永続化未設定  
3. **セキュリティ**: 本番環境向けセキュリティ設定要追加

## 🔗 重要なドキュメント

- **サンドボックス使用ガイド**: `backend/サンドボックス使用ガイド.md`
- **API仕様**: http://localhost:8000/docs (開発時)
- **テスト例**: `backend/test/example_usage.py`

## 📞 トラブルシューティング

### Docker関連
```bash
# コンテナ再起動
docker-compose down && docker-compose up --build

# ボリューム削除してクリーンビルド
docker-compose down -v && docker-compose up --build
```

### 依存関係エラー
```bash
# フロントエンド
cd frontend && npm cache clean --force && npm install

# バックエンド  
pip install -r backend/requirements.txt
```

---

**注意**: このプロジェクトは教育目的であり、本番環境では追加のセキュリティ対策が必要です。
