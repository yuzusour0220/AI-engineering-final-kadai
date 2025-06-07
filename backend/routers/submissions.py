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

    # サンドボックスでユーザーコード実行
    try:
        user_result = await execute_python_code_in_docker(
            user_code=exec_code,
            stdin_input=problem.test_input,  # test_inputを標準入力として渡す
        )

        # 正解コードも実行して結果を比較
        is_correct = False
        correct_result = None  # 正解コードの実行結果を保存
        try:
            # 正解コードを実行
            correct_exec_code = problem.correct_code
            if problem.correct_code.strip().startswith(("{", "<")):
                # 正解コードがnotebook形式の場合はPythonコードに変換
                try:
                    correct_exec_code = notebook_to_python(problem.correct_code)
                except Exception:
                    correct_exec_code = problem.correct_code

            correct_result = await execute_python_code_in_docker(
                user_code=correct_exec_code,
                stdin_input=problem.test_input,
            )

            # 標準出力を比較して正解判定
            user_stdout = user_result.stdout.strip() if user_result.stdout else ""
            correct_stdout = (
                correct_result.stdout.strip() if correct_result.stdout else ""
            )
            print(f"User stdout: {user_stdout}")
            print(f"Correct stdout: {correct_stdout}")
            is_correct = user_stdout == correct_stdout

        except Exception as e:
            print(f"正解コード実行時にエラー: {e}")
            # 正解コード実行でエラーが発生した場合は、エラーがなければ正解とみなす
            is_correct = user_result.exit_code == 0 and not user_result.stderr

        advice_text = await generate_advice_with_huggingface(
            problem_title=problem.title,
            problem_description=problem.description,
            user_code=user_code,
            execution_stdout=user_result.stdout,
            execution_stderr=user_result.stderr,
            correct_code=problem.correct_code,
            is_correct=is_correct,
        )

        # 提出を保存
        new_submission = SubmissionModel(
            problem_id=problem_id,
            user_code=user_code,
            stdout=user_result.stdout,
            stderr=user_result.stderr,
            execution_time_ms=user_result.execution_time_ms,
            exit_code=user_result.exit_code,
            advice_text=advice_text,
            is_correct=is_correct,
            submitted_at=datetime.now(timezone.utc),
        )
        db.add(new_submission)
        db.commit()

        # レスポンスを返す
        return SubmissionResponse(
            message="コードの実行が完了しました",
            stdout=user_result.stdout,
            stderr=user_result.stderr,
            execution_time_ms=user_result.execution_time_ms,
            exit_code=user_result.exit_code,
            advice_text=advice_text,
            is_correct=is_correct,
            # お手本の実行結果を追加
            correct_stdout=correct_result.stdout if correct_result else None,
            correct_stderr=correct_result.stderr if correct_result else None,
            correct_execution_time_ms=correct_result.execution_time_ms if correct_result else None,
        )

    except Exception as e:
        # 実行エラーの場合でも記録は残す
        new_submission = SubmissionModel(
            problem_id=problem_id,
            user_code=user_code,
            stderr=str(e),
            exit_code=-1,
            is_correct=False,
            submitted_at=datetime.now(timezone.utc),
        )
        db.add(new_submission)
        db.commit()

        return SubmissionResponse(
            message="コードの実行中にエラーが発生しました",
            stderr=str(e),
            exit_code=-1,
            is_correct=False,
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
