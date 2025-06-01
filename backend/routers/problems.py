from fastapi import APIRouter, HTTPException
from typing import List
from models import Problem
from datetime import datetime

# 関連するAPIエンドポイント（URL）をグループ化するために使われます。このルーターによって、問題に関するすべての操作がまとめられています。
router = APIRouter()

# インメモリデータストア
# 現時点での問題データを一時的に保存するための「インメモリデータストア」です。つまり、アプリケーションが実行されている間だけデータがメモリに保持され、アプリケーションを再起動するとデータは消えてしまいます。実際のアプリケーションでは、データベース（MongoDBやPostgreSQLなど）を使ってデータを永続化します。
problems_db: List[Problem] = []


@router.post("/problems/", response_model=Problem)
async def create_problem(problem: Problem):
    """新しい問題を作成する"""
    # 問題が既に存在するか確認
    for p in problems_db:
        if p.id == problem.id:
            raise HTTPException(
                status_code=400, detail=f"Problem with ID {problem.id} already exists"
            )

    # 現在時刻を設定
    problem.created_at = datetime.now(datetime.timezone.utc)
    problem.updated_at = problem.created_at

    # 問題を保存
    problems_db.append(problem)
    return problem


@router.get("/problems/", response_model=List[Problem])
async def read_problems():
    """全ての問題を取得する"""
    return problems_db


@router.get("/problems/{problem_id}", response_model=Problem)
async def read_problem(problem_id: int):
    """指定されたIDの問題を取得する"""
    for problem in problems_db:
        if problem.id == problem_id:
            return problem
    raise HTTPException(
        status_code=404, detail=f"Problem with ID {problem_id} not found"
    )


@router.put("/problems/{problem_id}", response_model=Problem)
async def update_problem(problem_id: int, updated_problem: Problem):
    """指定されたIDの問題を更新する"""
    for i, problem in enumerate(problems_db):
        if problem.id == problem_id:
            # IDが一致しているか確認
            if updated_problem.id != problem_id:
                raise HTTPException(
                    status_code=400, detail="Problem ID in path and body must match"
                )

            # 更新時刻を設定
            updated_problem.created_at = problem.created_at  # 作成日時は変更しない
            updated_problem.updated_at = datetime.now(datetime.timezone.utc)

            # 問題を更新
            problems_db[i] = updated_problem
            return updated_problem

    raise HTTPException(
        status_code=404, detail=f"Problem with ID {problem_id} not found"
    )


@router.delete("/problems/{problem_id}")
async def delete_problem(problem_id: int):
    """指定されたIDの問題を削除する"""
    for i, problem in enumerate(problems_db):
        if problem.id == problem_id:
            # 問題を削除
            problems_db.pop(i)
            return {
                "message": f"Problem with ID {problem_id} has been deleted successfully"
            }

    raise HTTPException(
        status_code=404, detail=f"Problem with ID {problem_id} not found"
    )
