# encoding: utf-8
# @File  : db_session.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/11

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from bot.config import DB_URL

# 初始化数据库连接:
engine = create_engine(DB_URL, echo=False)
# 创建DBSession类型:
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
