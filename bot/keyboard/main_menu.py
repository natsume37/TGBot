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


async def get_home_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🔥首页", callback_data="home_main"),
            InlineKeyboardButton("📰新闻", callback_data="home_news"),
            InlineKeyboardButton("👤我的", callback_data="home_profile")
        ],
        [InlineKeyboardButton("language", callback_data="home_language")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_profile_keyboard():
    keyboard = [
        [InlineKeyboardButton("返回", callback_data="home_back"),
         InlineKeyboardButton("➡️", callback_data="next_page")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_settings_menu_keyboard():
    keyboard = [
        [KeyboardButton("🔔 通知设置"), KeyboardButton("🔐 隐私设置")],
        [KeyboardButton("🔙 关闭页面")]  # 👈 返回按钮
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# 新闻接口下按钮
def get_news_keyboard():
    keyboard = [
        [InlineKeyboardButton("返回", callback_data="home_back"),
         InlineKeyboardButton("➡️", callback_data="next_page")],
    ]
    return InlineKeyboardMarkup(keyboard)
