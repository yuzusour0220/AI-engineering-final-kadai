# AIエンジニアリング最終課題

このリポジトリは、Python プログラミングの提出物を評価する Web アプリケーションです。
講座の最終課題として本アプリを開発しました。学生がブラウザ上でコードを書いて提出すると、
Docker サンドボックスで安全に実行し、結果をもとに Hugging Face API でアドバイスを生成します。
添削者は提出履歴と実行結果を確認し、生成されたコメントを参考に採点できます。

## 主な機能

- 問題一覧・詳細ページの表示
- コード編集と提出 (Python スクリプト / Jupyter Notebook)
- Docker サンドボックスによる安全なコード実行
- Hugging Face API を利用したフィードバック生成

## セットアップ

1. リポジトリをクローンします。
2. Docker が利用できる環境で次を実行してください。

```bash
docker-compose up --build
```

3. サンドボックス用イメージが無い場合、バックエンドが初回実行時に自動でビルドします。
   手動でビルドしたい場合は以下を実行してください。

```bash
cd backend/sandbox_docker
docker build -t python-sandbox .
```

4. フロントエンドは `http://localhost:3000`、API ドキュメントは `http://localhost:8000/docs` で確認できます。

## 評価の流れ

1. 学生は問題詳細ページでコードを作成し提出します。
2. バックエンドがコンテナ内でコードを実行し、標準出力やエラーを記録します。
3. 実行結果を元に Hugging Face API からアドバイス文を生成します。
4. 添削者は提出一覧から内容とアドバイスを確認し、得点をつけます。

## フォルダ構成 (抜粋)

```
frontend/   # Next.js 15 + TypeScript
backend/    # FastAPI / SQLAlchemy
└─ sandbox_docker/  # コード実行用 Dockerfile
```

課題データと提出情報は SQLite データベースに保存されます。

## テストの実行

Docker と API が起動している状態で次のテストを実行できます。

```bash
python backend/test/simple_sandbox_test.py
python backend/test/test_sandbox_complete.py
python backend/test/api_smoke_test.py
python backend/test/test_docker_basic.py
```

## ライセンス

このリポジトリは学習目的で公開しています。詳細は `LICENSE` を参照してください。
