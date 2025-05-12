# encoding: utf-8
# @File  : error.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/10
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}')
