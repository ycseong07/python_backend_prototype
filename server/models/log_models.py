from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from server.database.database import Base

# 인증 로그 테이블 모델
class Auth(Base):
    __tablename__ = 'auth'
    __table_args__ = {'schema': 'log'}

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    email = Column(String(50))
    full_name = Column(String(20))
    access_time = Column(DateTime, default=func.now())

# 유저 행동 로그 테이블 모델
class UserLog(Base):
    __tablename__ = 'user_log'
    __table_args__ = {'schema': 'log'}

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    action_type = Column(String(50))
    timestamp = Column(DateTime, default=func.now())