from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

load_dotenv()
# 데이터베이스 설정
# SQLALCHEMY_DATABASE_URL = "sqlite:///./database_ptmind.db"
SQLALCHEMY_DATABASE_URL = os.getenv("MYSQL_DATABASE_URL")

# #  SQLAlchemy 엔진 생성
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 엔진은 SQLAlchemy가 데이터베이스와 상호 작용할 때 사용하는 중요한 객체로, 데이터베이스 연결을 담당
# connect_args={"check_same_thread": False}는 SQLite 데이터베이스와의 연결 설정 중 하나로,
# 현재 스레드에서만 사용 가능하도록 설정
# create_engine은 커넥션 풀을 생성 => 데이터베이스 접속하는 객체를 일정수만큼만들어
# 돌려쓰는 방식으로 세션접속에 소요되는 시간 단축, 데이터베이스에 동시접속수 제어

# 데이터베이스 세션을 생성하는 sessionmaker 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# autocommit=False -> commit을 해야 변경사항 저장. 잘못저장되어도 rollback으로 취소가능

# SQLAlchemy 모델을 정의할 때 사용되는 베이스 클래스
Base = declarative_base()

# 아래 라인은 main파일에서 모델을 불러와서 해야 정상작동
# Base를 상속받은 모델이 지금은 명시가 안되어있음
# Base.metadata.create_all(bind=engine)


# 제너레이터에서는 차례대로 결과를 반환하고자 return 대신 yield 키워드를 사용한다.
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
