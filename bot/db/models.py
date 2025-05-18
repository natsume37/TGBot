from datetime import datetime, date
from enum import Enum
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Boolean,
    DateTime,
    Enum as SQLEnum,
    func, Date
)
from sqlalchemy.ext.declarative import declarative_base

# 声明基础类
Base = declarative_base()


class LanguageEnum(str, Enum):
    """
    用户语言枚举
    使用标准的小写 value，便于与前端及数据库交互
    """
    EN = 'en'
    ZH = 'zh'

    def __str__(self):
        return self.value


class User(Base):
    """
    用户表模型
    使用 SQLAlchemy 标准 Declarative 模式，字段使用常见约定
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, comment='主键')
    telegram_id = Column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
        comment='Telegram 用户唯一 ID'
    )
    telegram_name = Column(String(50), comment='Telegram 用户名')
    is_admin = Column(
        Boolean,
        default=False,
        nullable=False,
        comment='是否为管理员'
    )
    language = Column(
        SQLEnum(LanguageEnum, name='language_enum', native_enum=False),
        nullable=False,
        default=LanguageEnum.EN,
        comment='用户语言'
    )
    ai_token = Column(
        Integer,
        default=10,
        nullable=False,
        comment='AI 调用剩余次数'
    )
    is_block = Column(
        Boolean,
        default=False,
        nullable=False,
        comment='是否被屏蔽'
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment='创建时间'
    )


class SignIn(Base):
    __tablename__ = "sign_in"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    sign_date = Column(Date, nullable=False, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_days = Column(Integer, default=1)
    streak_days = Column(Integer, default=1)

