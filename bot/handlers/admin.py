# encoding: utf-8
# @File  : admin.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/18
from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from db.user import *
from db.db_session import AsyncSessionLocal
from db import user
from bot.keyboard.admin_keyboard import *
import logging

from bot.utils.tools import get_translator

logger = logging.getLogger(__name__)


@admin_only
async def han_root_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    弹出管理员菜单按钮
    :param update:
    :param context:
    :return:
    """
    lang_code = context.user_data.get("language", "en")
    _ = get_translator(lang_code)

    reply_markup = get_admin_menu()

    if update.message:
        logger.debug("message类型")
        await update.message.reply_text(
            text=_("请选择你的操作") + "👉️ /help；",
            reply_markup=reply_markup
        )
    elif update.callback_query:
        # logger.debug("callback类型按钮")
        await update.callback_query.edit_message_text(
            text=_("查看帮助👉️ /help；"),
            reply_markup=reply_markup
        )


@admin_only
async def tally_root_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inp = update.message.text
    from bot.services.server_ai import ChatGPTBot
    prompt = """你现在是一个个人财务管家。我会给你一段文本。请你依据用户输入 例如（今天买了一个水果花了6.9元，中午午饭吃了烤鸭饭花了14元。）
总结归纳用户每笔消费的消费类型，消费金额，以及小飞备注
严格安装格式化输出 例如（消费类型 吃饭 ，消费金额 14 ，备注 烤鸭饭 ）必须包含 消费类型 消费金额 以及备注！
    """
    bot = ChatGPTBot(prompt=prompt)
    res = await bot.chat(inp)
    await update.message.reply_text(
        text=res + '\n记账成功'
    )


if __name__ == '__main__':
    import asyncio


    async def main():
        inp = "今天买了一个黄瓜花了20元，买小飞老师的python网课花了200"
        from bot.services.server_ai import ChatGPTBot
        prompt = """你现在是一个个人财务管家。我会给你一段文本。请你依据用户输入 例如（今天买了一个水果花了6.9元，中午午饭吃了烤鸭饭花了14元。）
        总结归纳用户每笔消费的消费类型，消费金额，以及小飞备注
        严格安装格式化输出 例如（消费类型 吃饭 ,消费金额 14 ,备注 烤鸭饭 ）必须包含 消费类型 消费金额 以及备注！
            """
        bot = ChatGPTBot(prompt=prompt)
        res = await bot.chat(1234, inp)
        print(res)


    asyncio.run(main())
