# encoding: utf-8
# @File  : server_ai.py
# @Author: Martin
# @Desc : 
# @Date  :  2025/05/11
import asyncio
# openai_chatbot.py
import openai
from collections import defaultdict
from typing import List
from openai import OpenAIError

from bot.bot_config import Config

config = Config()


class ChatGPTBot:
    def __init__(self, api_key: str = config.OPEN_KEY, model: str = config.MODEL_TYPE,
                 prompt: str = config.SYSTEM_PROMPT):
        self.client = openai.AsyncOpenAI(api_key=api_key, base_url=config.OPEN_BASIC_URL)
        self.model = model
        self.sessions = defaultdict(list)  # user_id -> message list
        self.default_system_prompt = prompt

    def reset_session(self, user_id: int):
        self.sessions[user_id] = []

    def set_system_prompt(self, user_id: int, prompt: str):
        self.sessions[user_id] = [{"role": "system", "content": prompt}]

    async def chat(self, user_id: int, user_input: str) -> str:
        try:
            # 如果是第一次对话，添加默认 system prompt
            if not self.sessions[user_id]:
                self.sessions[user_id].append({"role": "system", "content": self.default_system_prompt})

            # 添加用户输入
            self.sessions[user_id].append({"role": "user", "content": user_input})

            # 发起请求
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=self.sessions[user_id],
                temperature=0.7
            )

            reply = response.choices[0].message.content
            self.sessions[user_id].append({"role": "assistant", "content": reply})
            return reply

        except OpenAIError as e:
            print(f"OpenAI Error: {e}")
            return "⚠️ 与 ChatGPT 通信时出错，请稍后重试。"
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return "⚠️ 出现未知错误，请联系管理员。"


# 运行


if __name__ == "__main__":
    async def main():
        # ✅ 替换为你自己的 OpenAI API Key
        bot = ChatGPTBot()

        user_id = 123456  # 模拟用户 ID

        print("默认模式测试：")
        response1 = await bot.chat(user_id, "你是谁？")
        print("Bot:", response1)

        response2 = await bot.chat(user_id, "你能干什么？")
        print("Bot:", response2)

        print("\n切换到开发者模式...")
        bot.set_system_prompt(user_id, "你是一个资深 Python 开发专家，请用专业术语回答问题。")

        response3 = await bot.chat(user_id, "请解释什么是 asyncio 和 await。")
        print("Bot:", response3)

        print("\n重置对话...")
        bot.reset_session(user_id)

        response4 = await bot.chat(user_id, "现在你还记得我说过什么吗？")
        print("Bot:", response4)


    asyncio.run(main())
