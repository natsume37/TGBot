# test_get_active_users.py
import asyncio
from bot.db.db_session import AsyncSessionLocal
from bot.db.models import User  # 修改路径以匹配你的结构
from bot.db.user import get_active_users  # 根据你的项目结构调整路径


async def test_active_users():
    # 调用目标函数
    users = await get_active_users(limit=10)

    if not users:
        print("⚠️ 没有活跃用户数据。")
        return

    print("📊 活跃用户前 10 名：\n")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user.telegram_name or '未知用户'} - 最近签到: {user.last_sign_date}")


if __name__ == "__main__":
    asyncio.run(test_active_users())
