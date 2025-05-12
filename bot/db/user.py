# encoding: utf-8
# @File  : user.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/11
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .models import User
from .db_session import SessionLocal
from bot.config import adminLog


def get_user(db: Session, telegram_id: int):
    return db.query(User).filter(User.telegram_id == telegram_id).first()


def add_user(db: Session, telegram_id: int, telegram_name: str,
             is_admin: bool = False, ai_token: int = 10):
    try:
        if get_user(db, telegram_id):
            return True
        new_user = User(
            telegram_id=telegram_id,
            telegram_name=telegram_name,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        adminLog.error(f"[add_user] Error: {e}")
        return False


def block_user(db: Session, telegram_id: User.telegram_id, is_block: User.is_block):
    try:
        user = get_user(db, telegram_id=telegram_id)
        if not user:
            adminLog.info("用户不存在、请添加用户后再锁定！")
            return None
        user.is_block = is_block
        db.commit()
        db.refresh(user)
        adminLog.debug(f"{user.telegram_id}账户已锁定")
        return True
    except SQLAlchemyError as e:
        db.rollback()
        adminLog.error(f"[add_user] Error: {e}")
        return False



