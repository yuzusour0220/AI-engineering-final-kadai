from pydantic import BaseModel
from datetime import datetime, timezone


class ProblemBase(BaseModel):
    """
    問題情報の基本モデル
    """

    title: str
    description: str
    correct_code: str
    test_input: str | None = None  # テストケース入力文字列


class ProblemCreate(ProblemBase):
    """
    問題作成時のモデル
    """

    pass  # IDは自動生成されるため、作成時には不要


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
    code_type: str = "python"  # "python" または "notebook"


class SubmissionResponse(BaseModel):
    """
    コード提出のレスポンスモデル
    """

    message: str
    stdout: str | None = None  # 実行標準出力
    stderr: str | None = None  # 実行標準エラー
    execution_time_ms: float | None = None  # 実行時間（ミリ秒）
    exit_code: int | None = None  # 終了コード
    advice_text: str | None = None  # AIからのアドバイス


class Submission(BaseModel):
    """
    提出情報を表すモデル
    """

    id: int
    problem_id: int
    user_code: str
    stdout: str | None = None
    stderr: str | None = None
    execution_time_ms: float | None = None
    exit_code: int | None = None
    advice_text: str | None = None
    submitted_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemyモデルからの変換を許可
