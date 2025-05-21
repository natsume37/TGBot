from datetime import date, datetime, timedelta
from typing import Optional, List
from sqlalchemy import select, insert, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import SignIn, User
from .db_session import AsyncSessionLocal

import logging

logger = logging.getLogger(__name__)


async def user_signed_in_on(db: AsyncSession, user_id: int, sign_date: date) -> bool:
    """检查用户指定日期是否已经签到"""
    stmt = select(SignIn).where(SignIn.user_id == user_id, SignIn.sign_date == sign_date)
    result = await db.execute(stmt)
    record = result.scalars().first()
    return record is not None


async def add_sign_in(db: AsyncSession, user_id: int, sign_date: Optional[date] = None):
    """
    新增签到记录。
    如果当天已经签到，返回 False。
    同时更新 User 表的 last_sign_date, streak_days, total_days
    """
    if sign_date is None:
        sign_date = date.today()

    # 先检查是否已经签到
    if await user_signed_in_on(db, user_id, sign_date):
        # logger.debug(f"User {user_id} already signed in on {sign_date}")
        return False, "你已经签过到了"

    try:
        # 插入签到记录
        new_sign = SignIn(user_id=user_id, sign_date=sign_date, created_at=datetime.utcnow())
        db.add(new_sign)

        # 获取用户信息，用于更新 streak 和 total
        user_stmt = select(User).where(User.telegram_id == user_id)
        user_res = await db.execute(user_stmt)
        user = user_res.scalars().first()
        if not user:
            # logger.error(f"User {user_id} not found when adding sign-in")
            await db.rollback()
            return False, "签到失败、请执行start命令重试"

        # 计算连续签到天数和累计签到天数
        last_date = user.last_sign_date
        if last_date == sign_date - timedelta(days=1):
            # 用户连续签到（用户上次签到时间等于昨天签到时间）
            user.streak_days += 1
        else:
            user.streak_days = 1

        user.total_days += 1
        user.last_sign_date = sign_date

        # 给亲到用户增加TOKEN次数
        user.ai_token += 5

        await db.commit()
        await db.refresh(user)
        # logger.debug(f"User {user_id} signed in on {sign_date}. Streak: {user.streak_days}, Total: {user.total_days}")
        return True, "签到成功"
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"[add_sign_in] Error adding sign-in for user {user_id}: {e}")
        return False, "服务器异常、稍后重试！"


async def get_user_signins(db: AsyncSession, user_id: int, limit: int = 10) -> List[SignIn]:
    """获取某用户最近的签到记录，默认最近10条"""
    stmt = (
        select(SignIn)
        .where(SignIn.user_id == user_id)
        .order_by(SignIn.sign_date.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    records = result.scalars().all()
    return records


async def get_sign_in_count(db: AsyncSession, user_id: int) -> int:
    """获取某用户的签到总次数"""
    stmt = select(func.count()).select_from(SignIn).where(SignIn.user_id == user_id)
    result = await db.execute(stmt)
    count = result.scalar_one()
    return count


async def get_sign_in_users_on_date(db: AsyncSession, sign_date: date) -> List[int]:
    """获取指定日期所有签到用户的 user_id 列表"""
    stmt = select(SignIn.user_id).where(SignIn.sign_date == sign_date)
    result = await db.execute(stmt)
    user_ids = result.scalars().all()
    return user_ids


# 方便外部调用的接口，自动创建会话

async def sign_in_user(user_id: int, sign_date: Optional[date] = None) -> bool:
    async with AsyncSessionLocal() as db:
        return await add_sign_in(db, user_id, sign_date)


async def get_recent_user_signins(user_id: int, limit: int = 10) -> List[SignIn]:
    async with AsyncSessionLocal() as db:
        return await get_user_signins(db, user_id, limit)


async def count_user_signins(user_id: int) -> int:
    async with AsyncSessionLocal() as db:
        return await get_sign_in_count(db, user_id)


async def users_signed_in_on(sign_date: date) -> List[int]:
    async with AsyncSessionLocal() as db:
        return await get_sign_in_users_on_date(db, sign_date)
