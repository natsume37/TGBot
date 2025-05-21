# encoding: utf-8
# @File  : main.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/21
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/api/data")
async def get_data():
    return {
        "x": [1, 2, 3, 4, 5],
        "y": [10, 15, 13, 17, 21]
    }
