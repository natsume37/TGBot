# encoding: utf-8
# @File  : admin_keyboard.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/19
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_admin_menu():
    keyboard = [
        [
            InlineKeyboardButton("🔥主菜单", callback_data="admin_main_menu"),
            InlineKeyboardButton("📰查询用户", callback_data="admin_show_userid"),
            InlineKeyboardButton("👤我的", callback_data="admin_block_user")
        ],
        [InlineKeyboardButton("language", callback_data="admin_language")],
    ]
    return InlineKeyboardMarkup(keyboard)
