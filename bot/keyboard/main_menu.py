# encoding: utf-8
# @File  : main_menu.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/10
# bot/handlers/menu.py
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.utils.tools import get_translator


def get_main_button(lang_code: str) -> ReplyKeyboardMarkup:
    """
    根据用户语言动态生成主菜单按钮。
    :param lang_code: 'en' 或 'zh'
    """
    # 1. 拉取对应语言的翻译函数
    _ = get_translator(lang_code)

    keyboard = [
        [
            KeyboardButton(f"🔥{_('首页')}"),
            KeyboardButton(f"📰{_('新闻')}"),
            KeyboardButton(f"👤{_('我的')}")
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_profile_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎁 一键分享", callback_data="share"),
         InlineKeyboardButton("➡️", callback_data="next_page")],
        [InlineKeyboardButton("💵 收益提现", callback_data="withdraw"),
         InlineKeyboardButton("💰 邀请赚钱", callback_data="invite")],
        [InlineKeyboardButton("🔍 搜索设置", callback_data="search_settings"),
         InlineKeyboardButton("📎 提交收录", callback_data="submit")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def show_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "这是您的信息：xxxxxxx",
        reply_markup=ReplyKeyboardRemove()  # 👈 移除键盘
    )


def get_settings_menu_keyboard():
    keyboard = [
        [KeyboardButton("🔔 通知设置"), KeyboardButton("🔐 隐私设置")],
        [KeyboardButton("🔙 关闭页面")]  # 👈 返回按钮
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
