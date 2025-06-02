from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
import os

# データベースファイルのパス
DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")

# SQLiteデータベースエンジンを作成
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# セッションファクトリを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルの基底クラスを作成
Base = declarative_base()


# データベースモデルの定義
class ProblemModel(Base):
    """
    問題情報を格納するデータベースモデル
    """

    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    correct_code = Column(Text)
    test_input = Column(String, nullable=True)  # テストケース入力文字列
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )


class SubmissionModel(Base):
    """
    提出情報を格納するデータベースモデル
    """

    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    problem_id = Column(Integer, index=True)
    user_code = Column(Text)
    stdout = Column(Text, nullable=True)  # 実行標準出力
    stderr = Column(Text, nullable=True)  # 実行標準エラー
    execution_time_ms = Column(Float, nullable=True)  # 実行時間（ミリ秒）
    exit_code = Column(Integer, nullable=True)  # 終了コード
    advice_text = Column(Text, nullable=True)  # AIからのアドバイス保存用
    submitted_at = Column(DateTime, default=datetime.now(timezone.utc))


# データベーステーブルを作成
def create_tables():
    Base.metadata.create_all(bind=engine)


# DBセッションを取得するヘルパー関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
