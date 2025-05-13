# encoding: utf-8
# @File  : menu.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/10
# bot/handlers/menu.py
import telegram
from telegram import BotCommand
from telegram.ext import Application

from ..keyboard.main_menu import *
from bot.db.db_session import SessionLocal
from bot.db import user
from bot.utils.tools import get_translator
from bot.config import adminLog


async def set_bot_commands(application: Application) -> None:
    """
    全局命令设置
    :param application:
    :return:
    """
    lang_code = 'zh'  # 默认中文
    _ = get_translator(lang_code)
    commands = [
        BotCommand("start", _("🔛开始")),
        BotCommand("help", _("💁帮助信息")),
        BotCommand("language", _("语言设置")),
        BotCommand("news", _("📰隔夜新闻"))
    ]
    await application.bot.set_my_commands(commands=commands)


async def show_settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚙️ 设置菜单：请选择一项",
        reply_markup=get_settings_menu_keyboard()
    )


async def about_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_obj = update.effective_user
    try:
        with user.SessionLocal() as db:
            userdb = user.get_user(db, user_obj.id)
            message = (
                f"<b>{user_obj.full_name}</b>\n"
                f"👤 <b>我的</b>\n\n"
                f"<b>昵称：</b>{user_obj.username or '无'}\n"
                f"<b>ID：</b><code>{user_obj.id}</code>\n\n"
                f"💵 AITOKEN：{userdb.ai_token}\n"
            )
    except Exception as e:
        message = f"<b>请点击 /star 命令、初始化账户</b>"

    await update.message.reply_html(
        message,
        reply_markup=get_profile_keyboard()
    )
