from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from domain.user import user_schema
from domain.user.user_schema import UserCreate
from domain.user.user_crud import authenticate_user, get_user_by_email

from util.csrf_manager import generate_csrf_token
from model import User
import time

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c"
ALGORITHM = "HS256"


router = APIRouter(
    prefix="/user",
)

# response 모델 대신 status_code로 주는건 클라이언트에게 정보를 보낼 필요가 없을때 씀


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def create_user(newuser: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == newuser.id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this ID already exists.")
    existing_email = db.query(User).filter(User.email == newuser.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email is already registered")
    db_user = User(**newuser.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 생성하므로 공집합
    mentor_ids = []
    # 만약 이미 생성된 유저면 이렇게 참조 필드에서 가져옴
    # mentor_ids = [mentor.id for mentor in db_user.mentors]
    return None


# CSRF요청 엔드포인트 ,CSRF라고  명시하지 않는게 나음
@router.get("/init")
def get_csrf_token():
    token = generate_csrf_token()
    return {"csrf_token": token}


@router.get("/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # 이메일로 사용자 조회
    user = get_user_by_email(
        db, form_data.username
    )  # 'username' 필드에 이메일이 들어옵니다.

    if not user or not authenticate_user(db, form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # JWT 페이로드 생성
    data = {
        "sub": user.email,  # 이메일을 서브젝트로 사용
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    # JWT 토큰 생성
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    success_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"LOGIN SUCCESS - Email: {user.email} - Time: {success_time}")
    # 토큰 반환
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user.email,  # 이메일 반환
    }
