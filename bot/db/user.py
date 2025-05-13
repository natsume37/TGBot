# encoding: utf-8
# @File  : user.py
# @Author: Martin
# @Desc :
# @Date  : 2025/05/11 (refactored)
from typing import Optional, Union

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .models import User, LanguageEnum
from .db_session import SessionLocal
from bot.config import adminLog


def get_user(db: Session, telegram_id: int) -> Optional[User]:
    """
    获取用户对象
    :param db:
    :param telegram_id:
    :return:
    """
    return db.query(User).filter(User.telegram_id == telegram_id).first()


def add_user(
        db: Session,
        telegram_id: int,
        telegram_name: str,
        is_admin: bool = False,
        ai_token: int = 10,
) -> Union[User, bool]:
    """
    添加用户
    :param db:
    :param telegram_id:
    :param telegram_name:
    :param is_admin:
    :param ai_token:
    :return:
    """
    try:
        existing = get_user(db, telegram_id)
        if existing:
            return existing

        new_user = User(
            telegram_id=telegram_id,
            telegram_name=telegram_name,
            is_admin=is_admin,
            ai_token=ai_token,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        adminLog.error(f"[add_user] Error: {e}")
        return False


def update_user_block_status(
        db: Session,
        telegram_id: int,
        is_block: bool,
) -> bool:
    """
    更新用户账号状态
    :param db:
    :param telegram_id:
    :param is_block:
    :return:
    """
    try:
        user = get_user(db, telegram_id)
        if not user:
            adminLog.info("User not found; please add before blocking")
            return False

        user.is_block = is_block
        db.commit()
        db.refresh(user)
        adminLog.debug(f"User {telegram_id} block status set to {is_block}")
        return True
    except SQLAlchemyError as e:
        db.rollback()
        adminLog.error(f"[set_user_block_status] Error: {e}")
        return False


def update_user_language(
        telegram_id: int,
        new_lang: Union[str, LanguageEnum],
) -> bool:
    """
    更新用户的语言、自动检查方便后期插入
    :param telegram_id:
    :param new_lang:
    :return:
    """
    with SessionLocal() as db:
        try:
            user = get_user(db, telegram_id)
            if not user:
                adminLog.info("用户未找到")
                return False

            if isinstance(new_lang, str):
                try:
                    lang_enum = LanguageEnum(new_lang.lower())
                except ValueError:
                    adminLog.error(f"Invalid language code: {new_lang}")
                    return False
            else:
                lang_enum = new_lang

            user.language = lang_enum
            db.commit()
            adminLog.debug(f"Updated user.language = {user.language}")
            return True
        except SQLAlchemyError as e:
            db.rollback()
            adminLog.error(f"[update_user_language] Error: {e}")
            return False
