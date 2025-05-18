# encoding: utf-8
# @File  : keyboard_callback.py
# @Author: Martin
# @Desc : 按键回调函数
# @Date  :  2025/05/14

from bot.handlers.handlers import *
from bot.db import user  # 假设 user 是你写的用户操作模块
from bot.db.db_session import AsyncSessionLocal
from telegram import BotCommand, BotCommandScopeChat, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from telegram import Update

import logging

logger = logging.getLogger(__name__)


async def home_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("回调信息被执行")
    query = update.callback_query
    await query.answer()
    date = query.data
    if date == "home_main":
        await home_command(update, context)
    elif date == "home_news":
        await news_command(update, context)
    elif date == "home_profile":
        await about_user(update, context)
    elif date == "home_language":
        await language_command(update, context)
    elif date == "home_back":
        await home_command(update, context)
    else:
        await update.effective_message.reply_text("未知的菜单选项")


# 按钮 en/zn触发
async def language_button_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang_code = query.data
    telegram_id = query.from_user.id

    async with AsyncSessionLocal() as db:
        userdb = await user.get_user(db, telegram_id)
        if userdb and lang_code == userdb.language.value:
            await query.edit_message_text(text="✅ 已是当前语言设置。")
            return

        logger.debug(f'语言设置被调用 lang_code: {lang_code}')

        success = await user.update_user_language(telegram_id, lang_code)
        if not success:
            await query.edit_message_text(text="❌ 语言切换失败，请稍后重试。")
            return

    _ = get_translator(lang_code)
    logger.debug(f"用户语言为：{lang_code}")
    # 删除原消息（含按钮），防止重复点击
    try:
        await context.bot.delete_message(
            chat_id=telegram_id,
            message_id=query.message.message_id
        )
    except Exception as e:
        logger.debug(f"❗️删除语言选择消息失败: {e}")
    # 更新命令
    commands = [
        BotCommand("start", f'▶️{_("开始")}'),
        BotCommand("help", f'💁{_("帮助信息")}'),
        BotCommand("language", f'🌏️{_("语言设置")}'),
        BotCommand("news", f'📰{_("隔夜新闻")}')
    ]
    scope = BotCommandScopeChat(chat_id=telegram_id)
    await context.bot.set_my_commands(commands=commands, scope=scope, language_code=lang_code)

    # 回复主按钮菜单
    reply_markup = get_main_button(lang_code)

    # 一次性回复完整的设置结果
    await context.bot.send_message(
        chat_id=telegram_id,
        text="\n".join([
            "✅ " + _("语言设置已更新成功！"),
            _("当前语言：{lang}").format(lang=_("中文") if lang_code == 'zh' else _("English")),
        ]),
        reply_markup=reply_markup
    )

    logger.debug(f"已为用户 {telegram_id} 应用语言：{lang_code}")
