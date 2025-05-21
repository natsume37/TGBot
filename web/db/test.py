# encoding: utf-8
# @File  : test.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/21

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, DECIMAL
from bot.db.db_models import Expense, Category  # 你的模型
from your_project.db_session import get_async_session  # 你的依赖注入获取session
import plotly.graph_objs as go
import plotly.io as pio


async def get_expense_pie_chart_html(session: AsyncSession, user_id: int) -> str:
    total_subq = (
        select(func.sum(Expense.amount))
        .where(Expense.user_id == user_id)
        .scalar_subquery()
    )

    stmt = (
        select(
            Expense.category_id,
            Category.name.label("category_name"),
            func.sum(Expense.amount).label("category_total"),
            (func.sum(Expense.amount) / cast(total_subq, DECIMAL(10, 2)) * 100).label("percentage")
        )
        .join(Category, Expense.category_id == Category.id)
        .where(Expense.user_id == user_id)
        .group_by(Expense.category_id, Category.name)
        .order_by(func.sum(Expense.amount).desc())
    )

    result = await session.execute(stmt)
    rows = result.all()

    labels = [row.category_name for row in rows]
    values = [float(row.category_total) for row in rows]

    # 使用 Plotly 构造饼图
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        hoverinfo='label+percent+value',
        textinfo='label+percent',
        textfont_size=14,
    )])

    fig.update_layout(
        title_text=f'用户 {user_id} 消费分类饼图',
        annotations=[dict(text='消费', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    # 生成完整HTML
    html_str = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
    return html_str
