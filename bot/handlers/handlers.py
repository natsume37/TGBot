# encoding: utf-8
# @File  : handlers.py
# @Author: Martin
# @Desc :
# @Date  :  2025/05/10
from ..config import setup_logging
from ..services import *
from bot.handlers.menu import *

from bot.db.db_session import AsyncSessionLocal
from bot.db import user
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update, BotCommand, BotCommandScopeChat, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from bot.db.sign_in import *

# 加载日志配置
setup_logging()
import logging

logger = logging.getLogger(__name__)


# Command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    start命令
    :param update:
    :param context:
    :return:
    """
    telegram_id = update.effective_user.id
    telegram_name = update.effective_user.username or update.effective_user.first_name

    async with AsyncSessionLocal() as db:
        await user.add_user(
            db,
            telegram_id=telegram_id,
            telegram_name=telegram_name
        )
        userdb = await user.get_user(db, telegram_id)
        lang_code = userdb.language.value if userdb and userdb.language else 'en'

    reply_markup = get_main_button(lang_code)

    await update.message.reply_text(
        "欢迎使用 Martin 私人助理",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    帮助菜单
    :param update:
    :param context:
    :return:
    """
    await update.message.reply_text("this is a test message about help")


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_fetcher = NewsFetcher()
    news = await news_fetcher.get_news()

    if update.message:
        await update.message.reply_text(
            news,
            reply_markup=get_news_keyboard()
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(news, reply_markup=get_news_keyboard())


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    语言功能
    :param update:
    :param context:
    :return:
    """
    keyboard = [
        [
            InlineKeyboardButton("中文", callback_data='zh'),
            InlineKeyboardButton("English", callback_data='en')
        ]
    ]

    try:
        async with AsyncSessionLocal() as db:
            userdb = await user.get_user(db, update.effective_user.id)
            lang_code = userdb.language.value if userdb and userdb.language else 'en'
    except Exception as e:
        logger.error(
            f"菜单命令翻译错误，用户ID: {update.effective_user.id}, 错误信息: {e}"
        )
        lang_code = 'en'

    context.user_data["language"] = lang_code
    _ = get_translator(lang_code)
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            _("请选择你的语言" + '；'),
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            _("请选择你的语言" + '；'),
            reply_markup=reply_markup
        )


async def home_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_code = context.user_data.get("language", "en")
    _ = get_translator(lang_code)

    reply_markup = await get_home_keyboard()

    if update.message:
        logger.info("message类型")
        await update.message.reply_text(
            _("查看帮助👉️ /help；"),
            reply_markup=reply_markup
        )
    elif update.callback_query:
        logger.info("callback类型按钮")
        await update.callback_query.edit_message_text(
            text=_("查看帮助👉️ /help；"),
            reply_markup=reply_markup
        )


async def auto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"you enter is {context}")


async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await update.message.chat.send_action(action="typing")

    try:
        reply = await chat_for_ai(update, context, user_input)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("请求出错了，请稍后再试。")
        logger.error(f"GPT请求错误：{e}")


async def chat_for_ai(update: Update, context: ContextTypes.DEFAULT_TYPE, user_input: str):
    telegram_id = update.effective_user.id

    try:
        async with AsyncSessionLocal() as db:
            user_obj = await user.get_user(db, telegram_id)

            if not user_obj:
                return "未找到用户，请先使用 /start 注册。"

            if user_obj.ai_token >= 1:
                bot = ChatGPTBot()
                res = await bot.chat(telegram_id, user_input)

                user_obj.ai_token -= 1
                await db.commit()

                return res
            else:
                return "积分不足，请联系管理员。"

    except Exception as e:
        logger.error(f"GPT 请求失败：{e}")
        return "处理出错"


# message-command
async def sign_in_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    签到功能
    :param update:
    :param context:
    :return:
    """
    async with AsyncSessionLocal() as db:
        code, msg = await add_sign_in(db, update.effective_user.id)

        await update.message.reply_text(text=msg)
