from fastapi import APIRouter
from typing import Dict
from models import SubmissionCreate

# コード提出に関するエンドポイントをグループ化するためのルーター
router = APIRouter()


@router.post("/submissions/")
async def create_submission(submission: SubmissionCreate) -> Dict[str, str]:
    """
    コード提出を受け付けるエンドポイント。
    現在は固定のメッセージを返すだけの実装。

    Args:
        submission: 提出されたコード情報

    Returns:
        メッセージを含む辞書
    """
    # TODO: 将来的にはここでコードの実行や評価を行う
    return {"message": "コードを受け付けました"}
