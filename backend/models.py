from pydantic import BaseModel
from datetime import datetime, timezone


class Problem(BaseModel):
    """
    問題情報を表すモデル
    """

    id: int
    title: str
    description: str
    correct_code: str
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)


class SubmissionCreate(BaseModel):
    """
    コード提出情報を表すモデル
    """

    problem_id: int
    user_code: str
