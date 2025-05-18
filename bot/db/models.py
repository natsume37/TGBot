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
    func,
    Date,
    UniqueConstraint,
    Index,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LanguageEnum(str, Enum):
    EN = "en"
    ZH = "zh"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, comment='主键')

    telegram_id = Column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
        comment='Telegram 用户唯一 ID'
    )

    telegram_name = Column(String(64), nullable=True, comment='Telegram 用户名')

    is_admin = Column(Boolean, default=False, nullable=False, comment='是否为管理员')

    language = Column(
        SQLEnum(LanguageEnum, name='language_enum', native_enum=False),
        nullable=False,
        default=LanguageEnum.EN,
        comment='用户语言'
    )

    ai_token = Column(Integer, default=10, nullable=False, comment='AI 调用剩余次数')

    is_block = Column(Boolean, default=False, nullable=False, comment='是否被屏蔽')

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment='创建时间'
    )

    last_sign_date = Column(Date, nullable=True, comment='最近签到日期')

    streak_days = Column(Integer, default=0, nullable=False, comment='连续签到天数')

    total_days = Column(Integer, default=0, nullable=False, comment='累计签到天数')


class SignIn(Base):
    __tablename__ = "sign_in"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(BigInteger, nullable=False, index=True, comment="Telegram 用户 ID（非外键）")

    sign_date = Column(Date, nullable=False, default=date.today, comment="签到日期")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="记录创建时间")

    # 联合唯一约束，确保每天只能签到一次
    __table_args__ = (
        UniqueConstraint("user_id", "sign_date", name="uq_user_date"),
        Index("idx_user_date", "user_id", "sign_date"),
    )
