# encoding: utf-8
# @File  : expense_manager.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/21
from pyg2plot import Plot
from sqlalchemy import select, update, delete, func, cast, DECIMAL
from datetime import date, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.db_session import AsyncSessionLocal, async_engine
from bot.db.models import Expense, Category  # 假设你把模型放在 models.py 中


# 新增消费记录
async def create_expense(user_id: int, category_id: int, amount: float, description: str = "",
                         payment_method: str = ""):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            expense = Expense(
                user_id=user_id,
                category_id=category_id,
                amount=amount,
                description=description,
                date=date.today(),
                payment_method=payment_method,
                created_at=datetime.utcnow(),
            )
            session.add(expense)
        await session.commit()
        return expense


# 查询某用户所有消费记录
async def get_user_expenses(user_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Expense).where(Expense.user_id == user_id).order_by(Expense.date.desc())
        )
        return result.scalars().all()


# 查询某用户指定时间段的消费记录
async def get_expenses_by_date_range(user_id: int, start_date: date, end_date: date):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Expense).where(
                Expense.user_id == user_id,
                Expense.date.between(start_date, end_date)
            )
        )
        return result.scalars().all()


# 修改消费记录（支持改金额和描述）
async def update_expense(expense_id: int, new_amount: float = None, new_description: str = None):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = update(Expense).where(Expense.id == expense_id)
            update_values = {}
            if new_amount is not None:
                update_values["amount"] = new_amount
            if new_description is not None:
                update_values["description"] = new_description

            if update_values:
                await session.execute(stmt.values(**update_values))
        await session.commit()


# 删除消费记录
async def delete_expense(expense_id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(delete(Expense).where(Expense.id == expense_id))
        await session.commit()





async def main():
    async with AsyncSessionLocal() as session:
        await get_expense_pie_chart_html(session, user_id=10001)

    await async_engine.dispose()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
