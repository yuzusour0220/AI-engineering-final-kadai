from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from sqlalchemy.orm import Session
from models import SubmissionCreate, SubmissionResponse
from database import get_db, SubmissionModel, ProblemModel
from datetime import datetime, timezone

# コード提出に関するエンドポイントをグループ化するためのルーター
router = APIRouter()


@router.post("/submissions/", response_model=SubmissionResponse)
async def create_submission(
    submission: SubmissionCreate, db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    コード提出を受け付けるエンドポイント。

    Args:
        submission: 提出されたコード情報
        db: データベースセッション

    Returns:
        メッセージを含む辞書
    """
    # 問題が存在するか確認
    problem = (
        db.query(ProblemModel).filter(ProblemModel.id == submission.problem_id).first()
    )
    if not problem:
        raise HTTPException(
            status_code=404, detail=f"Problem with ID {submission.problem_id} not found"
        )

    # 提出を保存
    new_submission = SubmissionModel(
        problem_id=submission.problem_id,
        user_code=submission.user_code,
        submitted_at=datetime.now(timezone.utc),
    )
    db.add(new_submission)
    db.commit()

    # TODO: 将来的にはここでコードの実行や評価を行う
    return {"message": "コードを受け付けました"}
