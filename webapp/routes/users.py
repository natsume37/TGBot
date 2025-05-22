# encoding: utf-8
# @File  : users.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/22

# routes/user.py
from fastapi import APIRouter, Request, Form, Query, Path
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy import select, update
from starlette.status import HTTP_302_FOUND
from sqlalchemy.exc import SQLAlchemyError

from db import AsyncSessionLocal, User, user

router = APIRouter()


@router.get("/users")
async def user_list(request: Request, page: int = Query(1, ge=1), per_page: int = 10):
    usersession = request.session.get("user")
    if not usersession:
        return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)

    try:
        async with AsyncSessionLocal() as db:
            users, total_users = await user.get_users_by_page(db, page, per_page)
            total_pages = (total_users + per_page - 1) // per_page

        return request.app.templates.TemplateResponse("users/users.html", {
            "request": request,
            "username": usersession,
            "users": users,
            "page": page,
            "total_pages": total_pages,
        })

    except SQLAlchemyError as e:
        print(f"[ERROR] 获取用户失败: {e}")
        return JSONResponse({"detail": "加载用户失败"}, status_code=500)


@router.get("/users/toggle_block/{user_id}")
async def toggle_block_user(user_id: int = Path(...)):
    new_status = None
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(User).where(User.id == user_id))
            user_obj = result.scalar_one_or_none()

            if not user_obj:
                return RedirectResponse(url="/users?msg=用户不存在", status_code=HTTP_302_FOUND)

            new_status = not user_obj.is_block
            stmt = update(User).where(User.id == user_id).values(is_block=new_status)
            await session.execute(stmt)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"[ERROR] toggle_block_user failed: {e}")
            return JSONResponse({"success": False, "message": "操作失败"}, status_code=500)

    msg = "已锁定用户" if new_status else "已解锁用户"
    return RedirectResponse(url=f"/users?msg={msg}", status_code=HTTP_302_FOUND)


@router.post("/users/update")
async def update_user_info(
        user_id: int = Form(...),
        is_admin: int = Form(...),
        ai_token: int = Form(...),
):
    async with AsyncSessionLocal() as session:
        try:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(
                    is_admin=bool(is_admin),
                    ai_token=ai_token
                )
            )
            await session.execute(stmt)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"[ERROR] update_user_info failed: {e}")
            return JSONResponse({"success": False, "message": "更新失败"}, status_code=500)

    return RedirectResponse(url="/users?msg=更新成功", status_code=HTTP_302_FOUND)
