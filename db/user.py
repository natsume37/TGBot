from typing import Optional, Union, List
from sqlalchemy import select, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User, LanguageEnum
from .db_session import AsyncSessionLocal
import logging

logger = logging.getLogger(__name__)


async def get_user(db: AsyncSession, telegram_id: int) -> Optional[User]:
    """异步获取用户对象"""
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalars().first()


async def add_user(
        db: AsyncSession,
        telegram_id: int,
        telegram_name: str,
        is_admin: bool = False,
        ai_token: int = 10,
) -> Union[User, bool]:
    """异步添加用户"""
    try:
        existing = await get_user(db, telegram_id)
        if existing:
            return existing

        new_user = User(
            telegram_id=telegram_id,
            telegram_name=telegram_name,
            is_admin=is_admin,
            ai_token=ai_token,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"[add_user] Error: {e}")
        return False


async def update_user_block_status(
        db: AsyncSession,
        telegram_id: int,
        is_block: bool,
) -> bool:
    """异步更新用户账号状态"""
    try:
        user = await get_user(db, telegram_id)
        if not user:
            logger.info("User not found; please add before blocking")
            return False

        user.is_block = is_block
        await db.commit()
        await db.refresh(user)
        # logger.debug(f"User {telegram_id} block status set to {is_block}")
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"[update_user_block_status] Error: {e}")
        return False


async def update_user_language(
        telegram_id: int,
        new_lang: Union[str, LanguageEnum],
) -> bool:
    """异步更新用户语言"""
    async with AsyncSessionLocal() as db:
        try:
            user = await get_user(db, telegram_id)
            if not user:
                logger.info("用户未找到")
                return False

            if isinstance(new_lang, str):
                try:
                    lang_enum = LanguageEnum(new_lang.lower())
                except ValueError:
                    logger.error(f"Invalid language code: {new_lang}")
                    return False
            else:
                lang_enum = new_lang

            user.language = lang_enum
            await db.commit()
            # logger.debug(f"Updated user.language = {user.language}")
            return True
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"[update_user_language] Error: {e}")
            return False


async def get_active_users(limit: int = 10) -> List[User]:
    """
    获取最近签到的活跃用户，按签到时间倒序排列，默认返回前10个。
    """
    async with AsyncSessionLocal() as db:
        try:
            stmt = (
                select(User)
                .where(User.last_sign_date.isnot(None))
                .order_by(desc(User.last_sign_date))
                .limit(limit)
            )
            result = await db.execute(stmt)
            users = result.scalars().all()
            logger.info(f"[get_active_users] 已获取最近活跃用户 Top{limit}")
            return users
        except SQLAlchemyError as e:
            logger.error(f"[get_active_users] 查询失败: {e}")
            return []
