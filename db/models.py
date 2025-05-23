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
    Index, DECIMAL,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


# --- 枚举定义 ---
class LanguageEnum(str, Enum):
    EN = "en"
    ZH = "zh"


# 支付方式枚举：使用英文值，在应用层做中文映射
class PaymentMethodEnum(str, Enum):
    ALIPAY = "ALIPAY"
    WECHAT = "WECHAT"
    BANK_CARD = "BANK_CARD"
    CASH = "CASH"
    OTHER = "OTHER"

    # 添加一个静态方法或字典来提供中文描述
    @staticmethod
    def to_chinese(method):
        mapping = {
            PaymentMethodEnum.ALIPAY: "支付宝",
            PaymentMethodEnum.WECHAT: "微信支付",
            PaymentMethodEnum.BANK_CARD: "银行卡转账",
            PaymentMethodEnum.CASH: "现金",
            PaymentMethodEnum.OTHER: "其他",
        }
        return mapping.get(method, str(method))  # 如果没有找到，返回其字符串值


# --- 用户表 (User) 定义 ---
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, comment='主键')
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True, comment='Telegram 用户唯一 ID')
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
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment='创建时间')
    last_sign_date = Column(Date, nullable=True, comment='最近签到日期')
    streak_days = Column(Integer, default=0, nullable=False, comment='连续签到天数')
    total_days = Column(Integer, default=0, nullable=False, comment='累计签到天数')
    password = Column(String(128), nullable=True, comment='登录密码（哈希值），默认允许为 null')


# --- 签到表 (SignIn) 定义 ---
class SignIn(Base):
    __tablename__ = "sign_in"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, index=True, comment="Telegram 用户 ID（非外键）")
    sign_date = Column(Date, nullable=False, default=date.today, comment="签到日期")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="记录创建时间")

    __table_args__ = (
        UniqueConstraint("user_id", "sign_date", name="uq_user_date"),
        Index("idx_user_date", "user_id", "sign_date"),
    )


# --- 类别表 (Category) 定义 ---
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, comment="分类主键")
    name = Column(String(100), nullable=False, comment="分类名称")
    parent_id = Column(Integer, nullable=True, index=True, comment="父级分类ID")
    level = Column(Integer, nullable=False, comment="分类等级：1为大类，2为子类")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,
                        comment='最后更新时间')

    def __repr__(self):
        return f"<Category(name={self.name}, level={self.level})>"

    __table_args__ = (
        Index("idx_category_parent_level", "parent_id", "level"),
    )


# --- 支出表 (Expense) 定义 ---
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    user_id = Column(BigInteger, nullable=False, index=True, comment="用户 Telegram ID")
    category_id = Column(Integer, nullable=False, index=True, comment="分类 ID")
    amount = Column(DECIMAL(10, 2), nullable=False, comment="消费金额")
    description = Column(String(255), nullable=True, comment="消费描述")
    date = Column(Date, nullable=False, default=date.today, index=True, comment="消费日期")
    # 支付方式枚举：使用英文值，在应用层做中文映射 (已省略 PaymentMethodEnum 定义，假设已在别处定义)
    payment_method = Column(
        SQLEnum(PaymentMethodEnum, name='payment_method_enum', native_enum=False),
        default=PaymentMethodEnum.OTHER,
        nullable=False,
        comment='支付方式'
    )
    currency = Column(String(10), default="CNY", nullable=False, comment="货币类型")
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, comment="记录创建时间")
    # updated_at 字段修改为可为空，并且不再有默认值
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True,
                        comment='最后更新时间')  # 默认就是 NULL

    def __repr__(self):
        return f"<Expense(user_id={self.user_id}, amount={self.amount}, category_id={self.category_id})>"

    __table_args__ = (
        Index("idx_user_date", "user_id", "date"),
        Index("idx_category_date", "category_id", "date"),
    )
