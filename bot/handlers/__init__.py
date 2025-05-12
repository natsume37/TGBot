# encoding: utf-8
# @File  : __init__.py.py
# @Author: Martin
# @Desc : 所有handlers模块
# @Date  :  2025/05/10
from telegram.ext import CommandHandler, MessageHandler, filters
from .handlers import *
from .menu import *


def get_commands():
    return [
        CommandHandler("start", start_command),
        CommandHandler("news", news_command)
    ]


def get_message_handles():
    return [
        MessageHandler(filters.TEXT & filters.Regex("我的"), about_user),
        MessageHandler(filters.TEXT & filters.Regex("📰新闻"), news_command),
        # AI 回复功能
        MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat),
    ]
