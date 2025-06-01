from fastapi import FastAPI
from routers import problems, submissions

app = FastAPI(title="課題管理API")

# ルーターを登録
app.include_router(problems.router, tags=["problems"])
app.include_router(submissions.router, tags=["submissions"])


@app.get("/")
async def root():
    return {
        "message": "課題管理APIへようこそ！ /docs にアクセスしてAPIドキュメントを確認してください。"
    }
