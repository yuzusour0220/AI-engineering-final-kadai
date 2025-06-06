from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models import Problem, ProblemCreate
from database import get_db, ProblemModel
from datetime import datetime, timezone

# 関連するAPIエンドポイント（URL）をグループ化するために使われます。
router = APIRouter()


@router.post("/problems/", response_model=Problem)
async def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
    """新しい問題を作成する"""
    # 問題をデータベースに保存（IDは自動生成）
    new_problem = ProblemModel(
        title=problem.title,
        description=problem.description,
        correct_code=problem.correct_code,
        test_input=problem.test_input,  # test_inputフィールドを追加
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)

    # Pydanticモデルに変換して返す
    return Problem(
        id=new_problem.id,
        title=new_problem.title,
        description=new_problem.description,
        correct_code=new_problem.correct_code,
        test_input=new_problem.test_input,  # test_inputフィールドを追加
        created_at=new_problem.created_at,
        updated_at=new_problem.updated_at,
    )


@router.get("/problems/", response_model=List[Problem])
async def read_problems(db: Session = Depends(get_db)):
    """全ての問題を取得する"""
    problems = db.query(ProblemModel).all()
    return [
        Problem(
            id=problem.id,
            title=problem.title,
            description=problem.description,
            correct_code=problem.correct_code,
            test_input=problem.test_input,  # test_inputフィールドを追加
            created_at=problem.created_at,
            updated_at=problem.updated_at,
        )
        for problem in problems
    ]


@router.get("/problems/{problem_id}", response_model=Problem)
async def read_problem(problem_id: int, db: Session = Depends(get_db)):
    """指定されたIDの問題を取得する"""
    problem = db.query(ProblemModel).filter(ProblemModel.id == problem_id).first()
    if problem is None:
        raise HTTPException(
            status_code=404, detail=f"Problem with ID {problem_id} not found"
        )
    return Problem(
        id=problem.id,
        title=problem.title,
        description=problem.description,
        correct_code=problem.correct_code,
        test_input=problem.test_input,  # test_inputフィールドを追加
        created_at=problem.created_at,
        updated_at=problem.updated_at,
    )


@router.put("/problems/{problem_id}", response_model=Problem)
async def update_problem(
    problem_id: int, updated_problem: ProblemCreate, db: Session = Depends(get_db)
):
    """指定されたIDの問題を更新する"""
    # 問題が存在するか確認
    db_problem = db.query(ProblemModel).filter(ProblemModel.id == problem_id).first()
    if db_problem is None:
        raise HTTPException(
            status_code=404, detail=f"Problem with ID {problem_id} not found"
        )

    # IDが一致しているか確認
    if updated_problem.id != problem_id:
        raise HTTPException(
            status_code=400, detail="Problem ID in path and body must match"
        )

    # 問題を更新
    db_problem.title = updated_problem.title
    db_problem.description = updated_problem.description
    db_problem.correct_code = updated_problem.correct_code
    db_problem.test_input = updated_problem.test_input  # test_inputフィールドを追加
    db_problem.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_problem)

    return Problem(
        id=db_problem.id,
        title=db_problem.title,
        description=db_problem.description,
        correct_code=db_problem.correct_code,
        test_input=db_problem.test_input,  # test_inputフィールドを追加
        created_at=db_problem.created_at,
        updated_at=db_problem.updated_at,
    )


@router.delete("/problems/{problem_id}")
async def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    """指定されたIDの問題を削除する"""
    # 問題が存在するか確認
    db_problem = db.query(ProblemModel).filter(ProblemModel.id == problem_id).first()
    if db_problem is None:
        raise HTTPException(
            status_code=404, detail=f"Problem with ID {problem_id} not found"
        )

    # 問題を削除
    db.delete(db_problem)
    db.commit()

    return {"message": f"Problem with ID {problem_id} has been deleted successfully"}
