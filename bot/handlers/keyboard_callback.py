# encoding: utf-8
# @File  : keyboard_callback.py
# @Author: Martin
# @Desc : 按键回调函数
# @Date  :  2025/05/14

from bot.handlers.handlers import *
from bot.config import adminLog


async def home_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理home命令按钮回调函数
    :param update:
    :param context:
    :return:
    """
    adminLog.info("回调信息被执行")
    query = update.callback_query
    await query.answer()
    date = query.data
    # 首页按钮
    if date == "home_main":
        await home_command(update, context)
    elif date == "home_news":
        await news_command(update, context)
    elif date == "home_profile":
        adminLog.info("此处")
        await about_user(update, context)
    elif date == "home_language":
        await language_command(update, context)
    elif date == "home_back":
        await home_command(update, context)
    else:
        await update.effective_message.reply_text("未知的菜单选项")


async def language_button_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # 告诉 Telegram 回调已处理（避免“正在加载”状态）
    await query.answer()
    # 'zh' 或 'en'
    lang_code = query.data

    telegram_id = query.from_user.id
    with user.SessionLocal() as db:
        userdb = user.get_user(db, telegram_id)
        if query == userdb.language.value:
            # 覆盖回复信息
            await context.bot.edit_message_text(
                chat_id=telegram_id,
                text="已完成"
            )
            return
    adminLog.debug(f'语言设置被调用 lang_code: {lang_code}')

    # 更新数据库
    success = update_user_language(telegram_id, lang_code)
    if not success:
        await query.edit_message_text(text="语言切换失败，请稍后重试。")
        return

    # 翻译函数
    _ = get_translator(lang_code)

    # 更新菜单命令（左边菜单）
    commands = [
        BotCommand("start", f'▶️{_("开始")}'),
        BotCommand("help", f'💁{_("帮助信息")}'),
        BotCommand("language", f'🌏️{_("语言设置")}'),
        BotCommand("news", f'📰{_("隔夜新闻")}'),
    ]
    # 私人命令翻译
    scope = BotCommandScopeChat(chat_id=telegram_id)
    await context.bot.set_my_commands(commands=commands, scope=scope, language_code=lang_code)
    # 先清空按钮（解决客户端缓存问题）
    await context.bot.send_message(
        chat_id=telegram_id,
        text=_("正在更新语言设置..."),
        reply_markup=ReplyKeyboardRemove()
    )
    # 刷新底部按钮
    reply_markup = get_main_button(lang_code)
    await context.bot.send_message(
        chat_id=telegram_id,
        text=_("语言已更改为：{lang}").format(lang=_("中文") if lang_code == 'zh' else _("English")),
        reply_markup=reply_markup,
    )

    adminLog.info(f"已为用户 {telegram_id} 应用语言：{lang_code}")
