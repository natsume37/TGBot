# encoding: utf-8
# @File  : handlers.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/10
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from ..utils.message_handle import handle_response
from ..services.news import NewsFetcher
from bot.services.server_ai import ChatGPTBot
from ..keyboard.main_menu import *
from ..services import *
from bot.db import user
from bot.config import adminLog


# Command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Start命令处理
    :param update:
    :param context:
    :return:
    """
    # 添加用户到数据库
    with user.SessionLocal() as db:
        user.add_user(db, update.effective_user.id, update.effective_user.name)
    await update.message.reply_text("欢迎使用Martin私人助理", reply_markup=get_main_button())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    help命令处理
    :param update:
    :param context:
    :return:
    """
    await update.message.reply_text("this is a test message about help")


async def auto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    自定义命令处理
    :param update:
    :param context:
    :return:
    """
    await update.message.reply_text(f"you enter is {context}")


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_fetcher = NewsFetcher()
    news = await news_fetcher.get_news()
    await update.message.reply_text(news or "获取新闻失败，请稍后再试")


# MessageHandler
async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await update.message.chat.send_action(action="typing")

    try:
        reply = await chat_for_ai(update, context, user_input)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("请求出错了，请稍后再试。")
        adminLog.error(f"GPT请求错误：{e}")


# Messages
async def chat_for_ai(update: Update, context: ContextTypes.DEFAULT_TYPE, user_input: str):
    telegram_id = update.effective_user.id

    try:
        with user.SessionLocal() as db:
            user_obj = user.get_user(db, telegram_id)

            if not user_obj:
                return "未找到用户，请先使用 /start 注册。"

            if user_obj.ai_token >= 1:
                bot = ChatGPTBot()
                res = await bot.chat(telegram_id, user_input)

                user_obj.ai_token -= 1
                db.commit()

                return res
            else:
                return "积分不足，请联系管理员。"

    except Exception as e:
        # 你可以用 logging.error 记录日志，这里简写返回异常文本
        adminLog.error(f"GPT 请求失败：{e}")
        return f"处理出错"
