from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from models import SubmissionCreate, SubmissionResponse
from database import get_db, SubmissionModel, ProblemModel
from services.sandbox_service import execute_python_code_in_docker, notebook_to_python
from services.advice_service import generate_advice_with_huggingface
from datetime import datetime, timezone

# コード提出に関するエンドポイントをグループ化するためのルーター
router = APIRouter()


async def _process_submission(
    *, problem_id: int, user_code: str, code_type: str, db: Session
) -> SubmissionResponse:
    """Problem existence check, code execution, advice generation, DB save."""
    # 問題が存在するか確認
    problem = db.query(ProblemModel).filter(ProblemModel.id == problem_id).first()
    if not problem:
        raise HTTPException(
            status_code=404, detail=f"Problem with ID {problem_id} not found"
        )

    # Notebookの場合はPythonコードに変換
    exec_code = user_code
    if code_type == "notebook":
        try:
            exec_code = notebook_to_python(user_code)
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
            user_code=user_code,
            execution_stdout=execution_result.stdout,
            execution_stderr=execution_result.stderr,
            correct_code=problem.correct_code,
        )

        # 提出を保存
        new_submission = SubmissionModel(
            problem_id=problem_id,
            user_code=user_code,
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
            problem_id=problem_id,
            user_code=user_code,
            stderr=str(e),
            exit_code=-1,
            submitted_at=datetime.now(timezone.utc),
        )
        db.add(new_submission)
        db.commit()

        return SubmissionResponse(
            message="コードの実行中にエラーが発生しました", stderr=str(e), exit_code=-1
        )


@router.post("/submissions/", response_model=SubmissionResponse)
async def create_submission(
    submission: SubmissionCreate, db: Session = Depends(get_db)
) -> SubmissionResponse:
    """JSON形式でコード提出を受け付けるエンドポイント"""
    return await _process_submission(
        problem_id=submission.problem_id,
        user_code=submission.user_code,
        code_type=submission.code_type,
        db=db,
    )


@router.post("/submissions/upload", response_model=SubmissionResponse)
async def create_submission_file(
    problem_id: int = Form(...),
    file: UploadFile = File(...),
    code_type: str = Form("python"),
    db: Session = Depends(get_db),
) -> SubmissionResponse:
    """ファイルアップロード形式でコード提出を受け付けるエンドポイント"""
    user_code_bytes = await file.read()
    try:
        user_code = user_code_bytes.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file encoding")

    return await _process_submission(
        problem_id=problem_id,
        user_code=user_code,
        code_type=code_type,
        db=db,
    )
