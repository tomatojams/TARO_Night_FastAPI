from fastapi import FastAPI, Request

# 유틸리티
import logging

# 미들웨어
from starlette.middleware.cors import CORSMiddleware
from util.middleware import ShowRequestMiddleware, CSRFMiddleware

# 라우터

from domain.user.user_router import router as user_router
from domain.AIchat.ai_router import router as ai_router


# 로깅세팅
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성 및 lifespan 설정, 미들웨어 추가
app = FastAPI()


app.add_middleware(ShowRequestMiddleware)
app.add_middleware(CSRFMiddleware)
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 라우터 추가
app.include_router(user_router)
app.include_router(ai_router)




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
