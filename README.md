# プログラミング課題システム

Pythonプログラミングの課題を解いて、AIからアドバイスを受けられるWebアプリケーションです。

## 📋 プロジェクト概要

学習者がPythonプログラミング課題に取り組み、コードを提出すると、AIが学習者のコードを分析してアドバイスを提供するシステムです。

## 🛠 技術スタック

### フロントエンド
- **Next.js 15** (App Router)
- **React 18** 
- **TypeScript**
- **Tailwind CSS**
- **Monaco Editor** (コードエディター)

### バックエンド
- **FastAPI** 
- **SQLAlchemy** (ORM)
- **SQLite** (データベース)
- **Pydantic** (データバリデーション)

### インフラ
- **Docker & Docker Compose**

## 🎯 実装済み機能の詳細

### フロントエンド実装

#### 1. **ホームページ (`/app/page.tsx`)**
- 問題一覧をカード形式で表示
- 各問題へのリンク（現在は問題1, 2をハードコード）
- 使い方説明セクション
- Tailwind CSSによるレスポンシブグリッドレイアウト

#### 2. **問題詳細ページ (`/app/problems/[id]/page.tsx`)**
- **動的ルーティング**: Next.js App Routerの`[id]`パラメータ使用
- **問題データ取得**: `useEffect`でAPI呼び出し、ローディング状態管理
- **2カラムレイアウト**: 左側に問題文、右側にコードエディター
- **エラーハンドリング**: API呼び出し失敗時の詳細エラー表示
- **コード提出フロー**:
  - 提出時にアドバイス表示エリアを表示
  - ローディング状態でスケルトンアニメーション
  - 提出完了後にアドバイス内容表示
  - `.py`だけでなく`.ipynb`形式のノートブックも送信可能

#### 3. **コンポーネント設計**
- **`AdviceDisplay.tsx`**: アドバイス表示専用コンポーネント
  - ローディング状態のスケルトンUI
  - `whitespace-pre-wrap`でテキスト整形
  - 条件分岐によるデフォルトメッセージ表示

#### 4. **API連携 (`/lib/api.ts`)**
- TypeScript型安全なAPI client実装
- カスタム`ApiError`クラスでエラーハンドリング
- 環境変数対応（`NEXT_PUBLIC_API_URL`）

#### 5. **型定義 (`/types/api.ts`)**
- フロントエンド・バックエンド間のインターフェース統一
- `Problem`, `SubmissionCreate`, `SubmissionResponse`型
  - `SubmissionCreate`では`code_type`フィールドでPythonかNotebookかを指定

### バックエンド実装

#### 1. **データベース設計 (`database.py`)**
- **SQLAlchemy ORM**による型安全なDB操作
- **テーブル定義**:
  ```python
  ProblemModel: id, title, description, correct_code, created_at, updated_at
  SubmissionModel: id, problem_id, user_code, submitted_at
  ```
- **`create_tables()`関数**: アプリケーション起動時の自動テーブル作成
- **依存性注入**: `get_db()`でセッション管理

#### 2. **API設計 (ルーター分割)**
- **`routers/problems.py`**: 問題CRUD操作
  - 全問題取得・特定問題取得・作成・更新・削除
  - HTTPステータスコード適切な設定
  - 存在チェックとエラーレスポンス
- **`routers/submissions.py`**: コード提出処理
  - 問題存在確認
  - 提出データのDB保存
  - UTC timezone対応
  - PythonスクリプトだけでなくJupyter Notebook(JSON形式)の提出にも対応

#### 3. **データモデル (`models.py`)**
- **Pydanticモデル**によるリクエスト/レスポンス検証
- **BaseModel継承**で型安全性確保
- フロントエンドの型定義と完全一致

#### 4. **CORS設定**
- フロントエンドとの通信許可
- 開発環境（localhost:3000）とDocker環境（frontend:3000）両対応

### インフラ実装

#### 1. **Docker設定**
- **フロントエンド**: Node.js 22-slim, Next.js本番ビルド
- **バックエンド**: Python 3.11-slim, uvicorn ASGI サーバー
- **docker-compose.yml**: サービス間通信設定

#### 2. **データ初期化機能 (`datainit.py`)**
- **問題データの自動投入**: 
  - 問題1: Hello World基礎課題
  - 問題2: 変数と計算課題
- **冪等性**: 既存データ確認後の重複回避
- **実際のPythonコード例**: 学習者向けの実践的サンプル
- **起動時実行**: コンテナ起動時の自動データセットアップ

#### 3. **データ初期化専用コンテナ (`data-init/`)**
- **独立したInitコンテナ**: メインアプリケーションと分離したデータセットアップ
- **`data-init/datainit.py`**: 
  - バックエンドと同じデータベースモデル使用
  - 問題データの一括投入スクリプト
  - エラーハンドリングと投入状況ログ
- **`data-init/Dockerfile`**: 軽量なPython実行環境
- **Docker Compose連携**: 
  - `depends_on`でバックエンド起動後に実行
  - 一度だけ実行される初期化専用サービス
  - データベース共有によるシームレスな初期化

## ❌ 未実装機能（重要度順）

### 🔴 最重要（MVP完成に必須）
1. **AIアドバイス生成**: OpenAI/Claude API連携未実装
2. **コード実行・評価**: Pythonコード実行環境未実装

### 🟡 重要（機能性向上）
3. **提出履歴管理**: 過去提出の表示・追跡未実装
4. **詳細エラー処理**: コード実行エラーの詳細表示未実装

### 🟢 補完機能
5. **ユーザー認証**: 個人管理機能未実装
6. **管理者機能**: 問題管理UI未実装

## 🏗 実装したアーキテクチャ

```
Frontend (Next.js)     Backend (FastAPI)        Database
┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐
│ /problems/[id]  │───►│ GET /problems/1 │───►│ ProblemModel│
│ Monaco Editor   │    │                 │    │             │
│ AdviceDisplay   │    │ POST /submissions│───►│ Submission  │
└─────────────────┘    └─────────────────┘    └─────────────┘
```

## 🚀 開発環境セットアップ

```bash
git clone <repository-url>
cd AI-engineering-final-kadai
docker-compose up --build

# アクセス先
# フロントエンド: http://localhost:3000
# バックエンドAPI: http://localhost:8000
# API文書: http://localhost:8000/docs
```

## 📁 実装済みファイル構造

```
AI-engineering-final-kadai/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx              # ホームページ
│   │   │   ├── layout.tsx            # アプリレイアウト
│   │   │   └── problems/[id]/page.tsx # 問題詳細
│   │   ├── components/
│   │   │   └── AdviceDisplay.tsx     # アドバイス表示
│   │   ├── lib/
│   │   │   └── api.ts               # API client
│   │   └── types/
│   │       └── api.ts               # 型定義
├── backend/
│   ├── routers/
│   │   ├── problems.py              # 問題API
│   │   └── submissions.py           # 提出API
│   ├── models.py                    # Pydanticモデル
│   ├── database.py                  # DB設定・ORM
│   ├── datainit.py                  # 初期データ投入
│   └── main.py                      # FastAPIアプリ
├── data-init/                       # データ初期化専用
│   ├── datainit.py                  # 初期データ投入スクリプト
│   └── Dockerfile                   # 初期化コンテナ
└── docker-compose.yml               # 開発環境
```

## 🚧 現在の制限事項

1. **固定アドバイスメッセージ**: AI生成機能未実装のため
2. **ハードコード問題リスト**: ホームページの問題一覧
3. **SQLiteファイル**: Docker再起動時のデータ永続化未設定
4. **セキュリティ**: コード実行のサンドボックス化なし

次の開発では **AIアドバイス生成機能** の実装が最優先です。
