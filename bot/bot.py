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


async def main():
    adminLog.info("BOT Star....")
    # Commands
    if proxy:
        app = Application.builder().token(BOT_TOKEN).proxy(proxy).build()
        adminLog.info(f"代理已启动proxy: {proxy}")
    else:
        app = Application.builder().token(BOT_TOKEN).build()
    # 初始化表
    models.Base.metadata.create_all(bind=engine)
    # Error
    app.add_error_handler(error)
    adminLog.info('Polling....')
    adminLog.debug("Enter CTR C Stop.....")

    await set_bot_commands(app)  # 设置命令菜单（自定义）
    for command in get_commands():
        app.add_handler(command)
    for message_handler in get_message_handles():
        app.add_handler(message_handler)
    app.run_polling(poll_interval=3, close_loop=False)


if __name__ == '__main__':
    asyncio.run(main())
