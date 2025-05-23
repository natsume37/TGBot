# encoding: utf-8
# @File  : expense_manager.py
# @Author: Martin
# @Desc :
# @Date  :  2025/05/21
import asyncio
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Dict

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from db.db_session import AsyncSessionLocal  # 假设这个文件已经正确设置了异步引擎和 sessionmaker
from db.models import Base, Expense, Category, PaymentMethodEnum  # 导入 Base 如果你在这里需要创建所有表


# -----------------------------
# Expense CRUD Functions (保持不变)
# -----------------------------

async def create_expense(
        user_id: int,
        category_id: int,
        amount: Decimal,
        description: Optional[str] = None,
        payment_method: Optional[PaymentMethodEnum] = None,
        expense_date: Optional[date] = None
) -> Expense:
    """
    创建一条新的支出记录。
    payment_method 参数现在应该传入 PaymentMethodEnum 枚举的英文成员 (e.g., PaymentMethodEnum.CASH)。
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            expense = Expense(
                user_id=user_id,
                category_id=category_id,
                amount=amount,
                description=description,
                payment_method=payment_method,
                date=expense_date if expense_date else date.today()
            )
            session.add(expense)
        await session.refresh(expense)
        return expense


async def get_user_expenses(user_id: int) -> List[Expense]:
    """
    获取指定用户的所有支出记录。
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Expense).where(Expense.user_id == user_id).order_by(Expense.date.desc(), Expense.created_at.desc())
        )
        return result.scalars().all()


async def get_expenses_by_date_range(
        user_id: int,
        start_date: date,
        end_date: date,
        limit: int = 20  # 默认最多返回 20 条记录
) -> List[Expense]:
    """
    获取指定用户在日期范围内的支出记录。
    """
    async with AsyncSessionLocal() as session:
        stmt = (
            select(Expense)
            .where(
                Expense.user_id == user_id,
                Expense.date.between(start_date, end_date)
            )
            .order_by(Expense.date.desc(), Expense.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()


async def update_expense(
        expense_id: int,
        new_amount: Optional[Decimal] = None,
        new_description: Optional[str] = None,
        new_payment_method: Optional[PaymentMethodEnum] = None  # 传入英文的 PaymentMethodEnum 成员
):
    """
    更新支出记录。
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = update(Expense).where(Expense.id == expense_id)
            update_values = {}
            if new_amount is not None:
                update_values["amount"] = new_amount
            if new_description is not None:
                update_values["description"] = new_description
            if new_payment_method is not None:
                update_values["payment_method"] = new_payment_method  # 直接使用英文的 PaymentMethodEnum 成员

            if update_values:
                await session.execute(stmt.values(**update_values))
        # 提交更改后，隐式地 commit 事务，无需再次 session.commit()


async def delete_expense(expense_id: int):
    """
    删除支出记录。
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(delete(Expense).where(Expense.id == expense_id))
        # 提交更改后，隐式地 commit 事务，无需再次 session.commit()


async def get_expenses_with_category(user_id: int) -> List[Dict]:
    """
    获取支出记录及其对应的分类名称，并转换支付方式为中文。
    """
    async with AsyncSessionLocal() as session:
        stmt = (
            select(Expense, Category.name)
            .join(Category, Expense.category_id == Category.id)
            .where(Expense.user_id == user_id)
            .order_by(Expense.date.desc())
        )
        result = await session.execute(stmt)
        return [
            {
                "id": e.id,  # 增加 id 字段方便后续操作
                "amount": e.amount,
                "category": cname,
                "description": e.description,
                "date": e.date,
                "payment_method_raw": e.payment_method.value,  # 原始英文值
                "payment_method_zh": PaymentMethodEnum.to_chinese(e.payment_method)  # 转换后的中文值
            }
            for e, cname in result.all()
        ]


async def get_expense_summary_by_category(user_id: int) -> List[Dict]:
    """
    获取指定用户按分类汇总的支出总额。
    """
    async with AsyncSessionLocal() as session:
        stmt = (
            select(Category.name, func.sum(Expense.amount).label("total"))
            .join(Category, Expense.category_id == Category.id)
            .where(Expense.user_id == user_id)
            .group_by(Category.name)
        )
        result = await session.execute(stmt)
        return [{"category": name, "total": float(total)} for name, total in result.all()]


# -----------------------------
# Category CRUD Functions (保持不变)
# -----------------------------

async def get_categories(level: Optional[int] = None) -> List[Category]:
    """
    获取所有分类，或指定等级的分类。
    """
    async with AsyncSessionLocal() as session:
        stmt = select(Category)
        if level is not None:
            stmt = stmt.where(Category.level == level)
        result = await session.execute(stmt.order_by(Category.level, Category.id))
        return result.scalars().all()


async def get_subcategories(parent_id: int) -> List[Category]:
    """
    获取指定父分类下的子分类。
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Category).where(Category.parent_id == parent_id)
        )
        return result.scalars().all()


async def create_category(name: str, level: int, parent_id: Optional[int] = None) -> Category:
    """
    创建新的分类。
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            category = Category(name=name, level=level, parent_id=parent_id)
            session.add(category)
        await session.refresh(category)
        return category


async def update_category(category_id: int, new_name: Optional[str] = None, new_parent_id: Optional[int] = None):
    """
    更新分类信息。
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = update(Category).where(Category.id == category_id)
            update_data = {}
            if new_name:
                update_data["name"] = new_name
            if new_parent_id is not None:
                update_data["parent_id"] = new_parent_id
            if update_data:
                await session.execute(stmt.values(**update_data))
        await session.commit()


async def delete_category(category_id: int):
    """
    删除分类。
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(delete(Category).where(Category.id == category_id))
        await session.commit()


# -----------------------------
# Main Execution for Testing (修改部分)
# -----------------------------
if __name__ == '__main__':
    from db.db_session import async_engine


    async def main():
        # 初始化数据库表（首次运行很重要）

        user_id = 10001  # 使用你的 SQL 数据中的用户 ID

        print("\n--- 测试：创建支出记录 ---")
        new_expense_id_1 = None
        try:
            exp1 = await create_expense(user_id, 101, Decimal('35.00'), '晚餐', PaymentMethodEnum.CASH,
                                        date(2025, 5, 23))
            print(
                f"成功创建支出：ID={exp1.id}，金额={exp1.amount}，方式={PaymentMethodEnum.to_chinese(exp1.payment_method)}")
            new_expense_id_1 = exp1.id
        except Exception as e:
            print(f"创建支出失败：{e}")

        new_expense_id_2 = None
        try:
            exp2 = await create_expense(user_id, 102, Decimal('12.50'), '咖啡', PaymentMethodEnum.ALIPAY,
                                        date(2025, 5, 24))
            print(
                f"成功创建支出：ID={exp2.id}，金额={exp2.amount}，方式={PaymentMethodEnum.to_chinese(exp2.payment_method)}")
            new_expense_id_2 = exp2.id
        except Exception as e:
            print(f"创建支出失败：{e}")

        print("\n--- 测试：按日期范围查询支出 ---")
        expenses_in_range = await get_expenses_by_date_range(
            user_id=user_id,
            start_date=date(2025, 5, 1),
            end_date=date(2025, 5, 25),
            limit=50
        )
        print(f"在指定日期范围内找到 {len(expenses_in_range)} 条支出记录。")
        # 可以选择性地打印详细信息，但这里为了简洁只打印数量。
        # 如果需要查看，可以循环打印：
        # for expense in expenses_in_range:
        #     print(f"  ID: {expense.id}, 日期: {expense.date}, 金额: {expense.amount}, "
        #           f"方式: {PaymentMethodEnum.to_chinese(expense.payment_method)}, 描述: {expense.description}")

        print("\n--- 测试：更新支出记录 ---")
        if new_expense_id_1:
            try:
                await update_expense(new_expense_id_1, new_amount=Decimal('40.00'), new_description='晚餐费用更新',
                                     new_payment_method=PaymentMethodEnum.WECHAT)
                print(f"成功更新支出 ID {new_expense_id_1}。")
                # 重新查询并打印更新后的信息，用于确认
                updated_expense_info = [exp for exp in (await get_expenses_with_category(user_id)) if
                                        exp['id'] == new_expense_id_1]
                if updated_expense_info:
                    info = updated_expense_info[0]
                    print(
                        f"  更新后信息：金额={info['amount']}，描述={info['description']}，方式={info['payment_method_zh']}")
            except Exception as e:
                print(f"更新支出 ID {new_expense_id_1} 失败：{e}")

        print("\n--- 测试：获取带分类和中文支付方式的支出列表 ---")
        expenses_with_categories = await get_expenses_with_category(user_id)
        print("以下是您的支出记录（包含分类和中文支付方式）：")
        for exp_dict in expenses_with_categories:
            print(f"  日期: {exp_dict['date']} | 金额: {exp_dict['amount']} | 分类: {exp_dict['category']} | "
                  f"方式: {exp_dict['payment_method_zh']} | 描述: {exp_dict['description'] or '无'}")

        print("\n--- 测试：获取按分类汇总的支出 ---")
        summary = await get_expense_summary_by_category(user_id)
        print("按分类汇总的支出：")
        for item in summary:
            print(f"  分类: {item['category']} | 总计: {item['total']:.2f}")

        print("\n--- 测试：删除支出记录 ---")
        if new_expense_id_2:
            try:
                await delete_expense(new_expense_id_2)
                print(f"成功删除支出 ID {new_expense_id_2}。")
            except Exception as e:
                print(f"删除支出 ID {new_expense_id_2} 失败：{e}")
        await async_engine.dispose()


    asyncio.run(main())
