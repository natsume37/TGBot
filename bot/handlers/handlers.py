# encoding: utf-8
# @File  : handlers.py
# @Author: Martin
# @Desc :
# @Date  :  2025/05/10
from telegram import Update, BotCommand, BotCommandScopeChat
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from ..utils.message_handle import handle_response
from ..services.news import NewsFetcher
from bot.services.server_ai import ChatGPTBot
from ..keyboard.main_menu import *
from ..services import *
from bot.db import user
from bot.db.user import *
from bot.config import adminLog
from ..utils.tools import get_translator
from bot.handlers.menu import *


# Command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start 命令处理
    """
    telegram_id = update.effective_user.id
    telegram_name = update.effective_user.username or update.effective_user.first_name

    # 1. 添加或获取用户，并立即查询 language
    with user.SessionLocal() as db:
        user.add_user(
            db,
            telegram_id=telegram_id,
            telegram_name=telegram_name
        )
        userdb = user.get_user(db, telegram_id)
        # 如果没查到，也给个默认值
        lang_code = userdb.language.value if userdb and userdb.language else 'en'

    # 2. 根据语言动态生成键盘下的菜单
    reply_markup = get_main_button(lang_code)

    # 3. 发送欢迎消息
    await update.message.reply_text(
        "欢迎使用 Martin 私人助理",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    help命令处理
    :param update:
    :param context:
    :return:
    """
    await update.message.reply_text("this is a test message about help")


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_fetcher = NewsFetcher()
    news = await news_fetcher.get_news()
    # 判断调用来源
    if update.message:
        await update.message.reply_text(
            news,
            reply_markup=get_news_keyboard()
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(news, reply_markup=get_news_keyboard())


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    语言设置指令、让用户修改语言
    :param update:
    :param context:
    :return:
    """
    # 创建语言选择的按钮
    keyboard = [
        [
            InlineKeyboardButton("中文", callback_data='zh'),
            InlineKeyboardButton("English", callback_data='en')
        ]
    ]
    try:
        with SessionLocal() as db:
            userdb = user.get_user(db, update.effective_user.id)
            if userdb and userdb.language:
                lang_code = userdb.language.value
            else:
                lang_code = 'en'
    except Exception as e:
        adminLog.error(
            f"菜单命令翻译错误，用户ID: {update.effective_user.id}, 错误信息: {e}"
        )
        lang_code = 'en'

    # 将用户的语言设置到上下文中、方便其他的handel直接使用不用频繁的调用数据库了

    context.user_data["language"] = lang_code
    # 获取翻译函数
    _ = get_translator(lang_code)

    # 设置键盘
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 回复消息并显示按钮
    await update.message.reply_text(
        _("请选择你的语言" + '；'),
        reply_markup=reply_markup
    )


async def home_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. 获取语言
    lang_code = context.user_data.get("language", "en")
    _ = get_translator(lang_code)

    reply_markup = await get_home_keyboard()

    # 添加按钮回调函数的复用
    if update.message:
        adminLog.info("message类型")
        await update.message.reply_text(
            _("查看帮助👉️ /help；"),
            reply_markup=reply_markup
        )

    # 支持callback_query
    elif update.callback_query:
        adminLog.info("callback类型按钮")
        await update.callback_query.edit_message_text(
            text=_("查看帮助👉️ /help；"),

            reply_markup=reply_markup
        )





async def auto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    自定义命令处理
    :param update:
    :param context:
    :return:
    """
    await update.message.reply_text(f"you enter is {context}")


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
