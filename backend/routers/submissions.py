from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import SubmissionCreate, SubmissionResponse
from database import get_db, SubmissionModel, ProblemModel
from services.sandbox_service import execute_python_code_in_docker, notebook_to_python
from services.advice_service import generate_advice_with_huggingface
from datetime import datetime, timezone

# コード提出に関するエンドポイントをグループ化するためのルーター
router = APIRouter()


@router.post("/submissions/", response_model=SubmissionResponse)
async def create_submission(
    submission: SubmissionCreate, db: Session = Depends(get_db)
) -> SubmissionResponse:
    """
    コード提出を受け付けるエンドポイント。

    Args:
        submission: 提出されたコード情報
        db: データベースセッション

    Returns:
        実行結果を含むSubmissionResponse
    """
    # 問題が存在するか確認
    problem = (
        db.query(ProblemModel).filter(ProblemModel.id == submission.problem_id).first()
    )
    if not problem:
        raise HTTPException(
            status_code=404, detail=f"Problem with ID {submission.problem_id} not found"
        )

    # Notebookの場合はPythonコードに変換
    exec_code = submission.user_code
    if submission.code_type == "notebook":
        try:
            exec_code = notebook_to_python(submission.user_code)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Notebook parsing error: {e}")

    # サンドボックスでコード実行
    try:
        execution_result = await execute_python_code_in_docker(
            user_code=exec_code,
            stdin_input=problem.test_input,  # test_inputを標準入力として渡す
        )

        advice_text = await generate_advice_with_huggingface(
            problem_title=problem.title,
            problem_description=problem.description,
            user_code=submission.user_code,
            execution_stdout=execution_result.stdout,
            execution_stderr=execution_result.stderr,
            correct_code=problem.correct_code,
        )

        # 提出を保存
        new_submission = SubmissionModel(
            problem_id=submission.problem_id,
            user_code=submission.user_code,
            stdout=execution_result.stdout,
            stderr=execution_result.stderr,
            execution_time_ms=execution_result.execution_time_ms,
            exit_code=execution_result.exit_code,
            advice_text=advice_text,
            submitted_at=datetime.now(timezone.utc),
        )
        db.add(new_submission)
        db.commit()

        # レスポンスを返す
        return SubmissionResponse(
            message="コードの実行が完了しました",
            stdout=execution_result.stdout,
            stderr=execution_result.stderr,
            execution_time_ms=execution_result.execution_time_ms,
            exit_code=execution_result.exit_code,
            advice_text=advice_text,
        )

    except Exception as e:
        # 実行エラーの場合でも記録は残す
        new_submission = SubmissionModel(
            problem_id=submission.problem_id,
            user_code=submission.user_code,
            stderr=str(e),
            exit_code=-1,
            submitted_at=datetime.now(timezone.utc),
        )
        db.add(new_submission)
        db.commit()

        return SubmissionResponse(
            message="コードの実行中にエラーが発生しました", stderr=str(e), exit_code=-1
        )
