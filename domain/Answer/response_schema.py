from pydantic import BaseModel


# 데이타베이스 이전것
class UserAnswer(BaseModel):

    user_id: str  # 필수필드
    user_answer: str


class AiAnswer(BaseModel):
    user_message: str
    input: str
    out_text: str
    text: dict


class ChatRoom(BaseModel):
    name: str
    titleName: str
    lastMessage: str = None
    imageExt: str
    profile: str
    beforeTime: str = None
    badge: int = None


class Mentor(BaseModel):
    ID: str
    gender: str
    name: str
    titleName: str
    slogan: str
    license: str
    career: str
    profile: str
    isFavorite: bool = False


# 데이타 베이스 이전
