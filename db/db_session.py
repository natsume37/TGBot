# encoding: utf-8
# @File  : db_session.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/11
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from bot.bot_config import Config

config = Config()
# 创建异步引擎
async_engine = create_async_engine("mysql+aiomysql://" + config.DB_URL)

# 同步引擎，用于建表【废弃】
# not_sync_engine = create_engine("mysql+pymysql://" + config.DB_URL, echo=True)
# 创建异步Session工厂，后续操作都使用 AsyncSession
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False  # 提交后不刷新实例，避免再次访问时去数据库加载
)

# 声明基类，所有模型继承它
Base = declarative_base()
