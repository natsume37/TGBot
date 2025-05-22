# encoding: utf-8
# @File  : main.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/21
# webapp/main.py
import os
from fastapi import FastAPI, Request, Form, Query, HTTPException, Path
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func, update
from starlette.middleware.sessions import SessionMiddleware
from starlette.status import HTTP_302_FOUND
from sqlalchemy.exc import SQLAlchemyError

from db import user, AsyncSessionLocal, User
from .routes import users as user_routes

app = FastAPI()

# 添加 Session 支持
app.add_middleware(SessionMiddleware, secret_key="Martin")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# 模板对象供子路由使用
app.templates = templates
# 路由注册
app.include_router(user_routes.router)


@app.get("/")
async def homepage(request: Request):
    user_session = request.session.get("user")
    if not user_session:
        return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)
    return templates.TemplateResponse("index.html", {"request": request, "username": user_session})


@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request, "error": None})


@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        userdb = await user.get_user_api(username)
    except SQLAlchemyError as e:
        print(f"[ERROR] login_post DB error: {e}")
        return templates.TemplateResponse("auth/login.html", {"request": request, "error": "服务器错误"})

    if not userdb or not userdb.is_admin or userdb.password != password:
        return templates.TemplateResponse("auth/login.html", {"request": request, "error": "用户名或密码错误"})
    request.session["user"] = username
    return RedirectResponse(url="/", status_code=HTTP_302_FOUND)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
