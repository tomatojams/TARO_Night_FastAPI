from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Integer,
    Text,
    Table,
    ForeignKey,
    Double,
    DATETIME,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base, engine


# SQLAlchemy 모델 정의
class User(Base):
    __tablename__ = "user"
    id = Column(String(length=50), primary_key=True, index=True)
    password = Column(String(length=100))
    is_Mentor = Column(Boolean, default=False, nullable=False)
    gender = Column(String(length=10), nullable=True)
    name = Column(String(length=100), nullable=False)
    email = Column(String(length=255), nullable=False, unique=True)
    phone = Column(String(length=20), nullable=True)
    joinDate = Column(DateTime, nullable=False, default=func.now())
    updateDate = Column(DateTime, nullable=True, onupdate=func.now())
    # 아래 users는 참조의 relation 이름 mentors는 상대방이 참조할 이름이나 없을때는 상대방의 테이블 네임
    mentors = relationship(
        "Mentor",
        secondary="user_mentor_history",
        back_populates="users",
        lazy="dynamic",  # 참조를 미리 읽어오면 DB에 과부하가 생길 수 있기 때문에 명시적으로 지연로딩을 함
    )


class Mentor(Base):
    __tablename__ = "mentor"
    id = Column(String(length=50), primary_key=True, index=True)
    gender = Column(String(length=10), nullable=False)
    name = Column(String(length=100), nullable=False)
    titleName = Column(String(length=100), nullable=True)
    slogan = Column(String(length=255), nullable=True)
    license = Column(String(length=100), nullable=False)
    career = Column(Integer, nullable=False)
    profile_add = Column(String(length=255), nullable=True)
    major = Column(String(length=255), nullable=False)
    users = relationship(
        "User",
        secondary="user_mentor_history",
        back_populates="mentors",
        lazy="dynamic",
    )


class Agency(Base):
    __tablename__ = "agency"
    id = Column(String(length=50), primary_key=True, index=True)


user_mentor_history = Table(
    "user_mentor_history",
    Base.metadata,
    Column("user_id", String(length=50), ForeignKey("user.id"), primary_key=True),
    Column("mentor_id", String(length=50), ForeignKey("mentor.id"), primary_key=True),
    Column("on_mentor", Boolean, nullable=False, default=False),
    Column("lately_on_mentor", DATETIME, nullable=False, onupdate=func.now()),
    Column("mentoring_count", Integer, nullable=False, default=0),
    Column("rating", Double, nullable=False, default=0),
)


class MqttMessage(Base):
    __tablename__ = "mqtt_messages"

    id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(String(length=50), ForeignKey("user.id"), nullable=False)
    # mentor_id = Column(String(length=50), ForeignKey("mentor.id"), nullable=False)
    # agency_id = Column(String(length=50), ForeignKey("agency.id"), nullable=False)
    topic = Column(String(length=255), index=True)
    payload = Column(Text)


# db파일 생성 engine 초기화
# Base를 상속받은 모든 모델의 metadata를 바탕으로 하므로 상속을 받은 모델들이 정해진 다음에
# db를 생성한다. 따라서 이 위치가 맞음
# Base.metadata.create_all(engine)
