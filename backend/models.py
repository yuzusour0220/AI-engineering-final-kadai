from pydantic import BaseModel
from datetime import datetime, timezone


class ProblemBase(BaseModel):
    """
    問題情報の基本モデル
    """

    title: str
    description: str
    correct_code: str


class ProblemCreate(ProblemBase):
    """
    問題作成時のモデル
    """

    id: int


class Problem(ProblemBase):
    """
    問題情報を表すモデル
    """

    id: int
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    class Config:
        from_attributes = True  # SQLAlchemyモデルからの変換を許可


class SubmissionCreate(BaseModel):
    """
    コード提出情報を表すモデル
    """

    problem_id: int
    user_code: str


class SubmissionResponse(BaseModel):
    """
    コード提出のレスポンスモデル
    """

    message: str
