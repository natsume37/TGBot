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


async def set_bot_commands(application: Application) -> None:
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Help info"),
        BotCommand('custom', '自定义功能'),
        BotCommand('news', '新闻功能')
    ]
    await application.bot.set_my_commands(commands=commands)


async def show_settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚙️ 设置菜单：请选择一项",
        reply_markup=get_settings_menu_keyboard()
    )


async def about_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = (
        f"<b>{user.full_name}</b>\n"
        f"👤 <b>我的</b>\n\n"
        f"<b>昵称：</b>{user.username or '无'}\n"
        f"<b>ID：</b><code>{user.id}</code>\n\n"
        f"💵 已提现：0$\n"
        f"💰 余额：0$\n"
        f"⏳ 待入账金额：0$"
    )
    await update.message.reply_html(
        message,
        reply_markup=get_profile_keyboard()
    )
