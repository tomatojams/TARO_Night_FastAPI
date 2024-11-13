from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
    ConfigDict,
    EmailStr,
)
from typing import Optional, List
from datetime import datetime
import bcrypt


class UserCreate(BaseModel):
    id: str
    password: str
    is_Mentor: bool = Field(default=False)
    gender: Optional[str] = None
    name: str
    email: EmailStr
    phone: Optional[str]
    joinDate: datetime
    updateDate: Optional[datetime]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="before")
    def hash_password(cls, values):
        password = values.get("password")
        if password:
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
            values["password"] = hashed.decode("utf-8")
        return values

    @field_validator("name")
    def check_not_empty(cls, v, field):
        if not v or not v.strip():
            raise ValueError(f"{field.name} cannot be empty")
        return v


class UserResponse(BaseModel):
    id: str
    gender: Optional[str]
    name: str
    email: str
    phone: Optional[str]
    joinDate: datetime
    updateDate: Optional[datetime]
    mentor_ids: List[str] = []

    model_config = ConfigDict(
        from_attributes=True,  # 속성에서 값을 읽고 쓸 수 있게 설정
        arbitrary_types_allowed=False,  # 타입 검사를 엄격히 수행
    )


# 토큰형식, 출력과 항목을 정확하게 맞춘다.


class Token(BaseModel):
    access_token: str
    token_type: str
    email: str
