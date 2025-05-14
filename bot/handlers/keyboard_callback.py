# encoding: utf-8
# @File  : keyboard_callback.py
# @Author: Martin
# @Desc : 按键回调函数
# @Date  :  2025/05/14

from bot.handlers.handlers import *
from bot.config import adminLog


async def home_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理home命令按钮回调函数
    :param update:
    :param context:
    :return:
    """
    query = update.callback_query
    await query.answer()
    date = query.data
    # 首页按钮
    if date == "home_main":
        await home_command(update, context)
    elif date == "home_news":
        await news_command(update, context)
    elif date == "home_profile":
        adminLog.info("此处")
        await about_user(update, context)
    elif date == "home_language":
        await language_command(update, context)
    else:
        await update.effective_message.reply_text("未知的菜单选项")
