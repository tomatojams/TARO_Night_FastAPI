from fastapi import APIRouter, HTTPException
from ai.ai import ai_init
from domain.Answer.response_schema import UserAnswer, AiAnswer
import logging
import traceback

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 라우터 설정
router = APIRouter(prefix="/aichat")

# ai 모델 초기화
try:
    chat = ai_init()
    user_data = {
        "user_message": f"첫인사 한글로 출력 + 날씨:{chat.weather}+ 현재시간:{chat.current_date_time}"
    }
    request_instance = chat.UserRequest(**user_data)
    answer = chat.gernerate_answer(request_instance)

    print(answer["answer"])
except Exception as e:
    logger.error(
        f"AI 초기화 또는 인사 처리 중 오류 발생: {e}\n{traceback.format_exc()}"
    )
    answer = {"answer": {"out_text": "서버오류", "text": "서버오류 입니다."}}

user_conv_list = []


@router.get("/pt")
async def read_pt():
    try:
        return answer["answer"]["out_text"]
    except KeyError as e:
        logger.error(
            f"read_pt 엔드포인트에서 KeyError 발생: {e}\n{traceback.format_exc()}"
        )
        raise HTTPException(status_code=500, detail="내부 서버 오류")


@router.get("/pt/")
async def read_pt_full():
    try:
        return answer["answer"]
    except KeyError as e:
        logger.error(
            f"read_pt_full 엔드포인트에서 KeyError 발생: {e}\n{traceback.format_exc()}"
        )
        raise HTTPException(status_code=500, detail="내부 서버 오류")


@router.get("/user_emotion")
async def read_user_emotion():
    try:
        return answer["answer"]["text"]
    except KeyError as e:
        logger.error(
            f"read_user_emotion 엔드포인트에서 KeyError 발생: {e}\n{traceback.format_exc()}"
        )
        raise HTTPException(status_code=500, detail="내부 서버 오류")


@router.post("/user/", response_model=AiAnswer)
async def create_user_item(user_answer: UserAnswer):
    try:
        user_conv_list.append(user_answer.dict())
        user_data = {
            "user_message": user_answer.user_answer,
        }
        request_instance = chat.UserRequest(**user_data)
        answer = chat.gernerate_answer(request_instance)
        print(answer["answer"]["out_text"])
        print(answer["answer"])
        return answer["answer"]
    except KeyError as e:
        logger.error(
            f"create_user_item 엔드포인트에서 KeyError 발생: {e}\n{traceback.format_exc()}"
        )
        raise HTTPException(status_code=500, detail="내부 서버 오류")
    except Exception as e:
        logger.error(
            f"create_user_item 엔드포인트에서 예기치 않은 오류 발생: {e}\n{traceback.format_exc()}"
        )
        raise HTTPException(status_code=500, detail="내부 서버 오류")
