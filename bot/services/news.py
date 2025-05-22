# utils/news.py
import asyncio
import logging
import re
import time
from datetime import datetime
from typing import Optional

import aiohttp
from lxml import etree


class NewsFetcher:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.week = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}
        self.url = "https://www.cls.cn/api/sw?app=CailianpressWeb&os=web&sv=7.7.5"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
        }
        self.payload = {
            "type": "telegram",
            "keyword": "你需要知道的隔夜全球要闻",
            "page": 0,
            "rn": 1,
            "os": "webapp",
            "sv": "7.7.5",
            "app": "CailianpressWeb"
        }

    async def get_news(self) -> Optional[str]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, headers=self.headers, data=self.payload) as resp:
                    json_data = await resp.json()
                    item = json_data["data"]["telegram"]["data"][0]
        except Exception as e:
            self.logger.error(f"获取新闻失败: {e}")
            return None

        news_text = item["descr"]
        timestamp = item["time"]
        ts = time.localtime(timestamp)
        weekday_news = datetime(*ts[:6]).weekday()

        weekday_now = datetime.now().weekday()
        if weekday_news != weekday_now:
            # 调用AI来总结回答
            try:
                from bot.services.server_ai import ChatGPTBot
                ai_news = ChatGPTBot(
                    prompt="请你给出最近发生的10条国内外热点新闻、总结提炼、回复简精炼！输出格式为：开头显示当前日期、第二行显示隔夜新闻四个字、最后再显示你总结的新闻！")
                res = await ai_news.chat(1010,
                                         "请给出今日新闻")
                return res
            except Exception as e:
                return "周日、周一暂无隔夜新闻"

        fmt_time = time.strftime("%Y年%m月%d日", ts)
        news_text = re.sub(r"(\d{1,2}、)", r"\n\1", news_text)

        plain_text = "".join(etree.HTML(news_text).xpath("//text()"))
        plain_text = re.sub(r"周[一二三四五六日]你需要知道的", "", plain_text)

        return f"{fmt_time} {self.week[weekday_news]}\n{plain_text}"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)


    async def main():
        fetcher = NewsFetcher()
        news = await fetcher.get_news()
        print(news or "暂无可用新闻")


    asyncio.run(main())
