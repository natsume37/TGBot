# encoding: utf-8
# @File  : bot.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/10
import asyncio
import signal

import nest_asyncio
from bot.config import BOT_TOKEN, adminLog, proxy
from bot.handlers import *
from bot.utils.error import error
from bot.handlers.menu import *
from bot.db.db_session import engine
from bot.db import models

# 补丁
nest_asyncio.apply()


def locate_update() -> Application:
    """
    统一加载app配置
    :return: app
    """
    if proxy:
        app = Application.builder().token(BOT_TOKEN).proxy(proxy).build()
        adminLog.info(f"代理已启动proxy: {proxy}")
    else:
        app = Application.builder().token(BOT_TOKEN).build()
    # 命令加载
    for command in get_commands():
        app.add_handler(command)

    # 消息类加载
    for message_handler in get_message_handles():
        app.add_handler(message_handler)

    # 按键回调函数加载
    for keyboard_callback in get_keyboard_callback():
        app.add_handler(keyboard_callback)
    return app


async def main():
    adminLog.info("BOT Star....")
    # Commands
    app = locate_update()
    # 初始化表
    models.Base.metadata.create_all(bind=engine)
    # Error
    app.add_error_handler(error)
    adminLog.info('Polling....')
    adminLog.debug("Enter CTR C Stop.....")

    # 自定义功能菜单设置
    await set_bot_commands(app)

    app.run_polling(poll_interval=3, close_loop=False)


if __name__ == '__main__':
    asyncio.run(main())
