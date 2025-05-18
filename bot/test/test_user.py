from bot.db.user import *
from sqlalchemy.orm import Session

if __name__ == '__main__':
    def main():
        # 使用 with 语法来确保会话关闭
        with AsyncSessionLocal() as db:

            telegram_id = 123456789
            telegram_name = "TestUser"

            print("🚀 尝试添加用户...")
            user = add_user(db, telegram_id=telegram_id, telegram_name=telegram_name)
            if user:
                print("✅ 用户添加结果:", user)
            else:
                print("❌ 添加用户失败")

            print("🚫 封禁用户...")
            result = update_user_block_status(db, telegram_id=telegram_id, is_block=True)
            if result:
                print("✅ 封禁操作成功")
            else:
                print("❌ 封禁操作失败")

            print("📄 查询用户...")
            u = get_user(db, telegram_id=telegram_id)
            if u:
                print("👤 当前用户：", u)
            else:
                print("❌ 用户未找到")


    main()
