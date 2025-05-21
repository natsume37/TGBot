# encoding: utf-8
# @File  : __init__.py.py
# @Author: Martin
# @Desc : 所有handlers模块
# @Date  :  2025/05/10
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackQueryHandler
from .handlers import *
from .menu import *
from .keyboard_callback import *
from .admin import *


def get_commands():
    return [
        CommandHandler("start", start_command),
        CommandHandler("help", help_command),
        CommandHandler("news", news_command),
        CommandHandler('language', language_command)
    ]


def get_message_handles():
    return [
        MessageHandler(filters.TEXT & filters.Regex('👤我的'), about_user),
        MessageHandler(filters.TEXT & filters.Regex("📰新闻"), news_command),
        MessageHandler(filters.TEXT & filters.Regex(r"🔥首页"), home_command),
        MessageHandler(filters.TEXT & filters.Regex(r"^#(签到|sign)"), sign_in_message),
        MessageHandler(filters.TEXT & filters.Regex(r"^#(id|ID)"), get_id_message),
        MessageHandler(filters.TEXT & filters.Regex(r"/ban"), han_root_command),
        # AI 回复功能
        MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat),

    ]


def get_keyboard_callback():
    return [
        # 语言命令回调
        CallbackQueryHandler(language_button_keyboard, pattern="^(zh|en)$"),
        CallbackQueryHandler(home_menu_callback, pattern="^home_"),
    ]
