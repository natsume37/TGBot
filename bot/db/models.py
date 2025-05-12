# encoding: utf-8
# @File  : models.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/11
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger

from .db_session import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    telegram_name = Column(String(20))
    is_admin = Column(Boolean, default=False, )
    ai_token = Column(Integer, default=10, nullable=False)
    is_block = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
