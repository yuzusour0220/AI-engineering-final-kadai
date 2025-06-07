from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import problems, submissions
from database import create_tables
import logging

logging.basicConfig(level=logging.INFO)

# データベーステーブルを作成
create_tables()

app = FastAPI(title="課題管理API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://frontend:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
        "*",  # 開発環境のため全許可（本番では制限すべき）
    ],  # Next.jsのサーバー
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを登録
app.include_router(problems.router, tags=["problems"])
app.include_router(submissions.router, tags=["submissions"])


@app.get("/")
async def root():
    return {
        "message": "課題管理APIへようこそ！ /docs にアクセスしてAPIドキュメントを確認してください。"
    }
