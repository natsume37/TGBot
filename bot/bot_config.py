import os
from dotenv import load_dotenv

load_dotenv()  # 加载.env文件


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        # 去除字符串两端空格，方便调用
        self.BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
        self.DB_URL = os.getenv("DB_URL", "").strip()
        self.PROXY = os.getenv("proxy", "").strip()
        self.OPEN_BASIC_URL = os.getenv("open_basic_url", "").strip()
        self.OPEN_KEY = os.getenv("open_key", "").strip()
        self.MODEL_TYPE = os.getenv("model_type", "").strip()
        self.SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "").strip()
        self.ENV = os.getenv("ENV", "production").strip().lower()
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").strip().upper()

    def is_dev(self):
        return self.ENV == "development"

    def is_prod(self):
        return self.ENV == "production"

    # 方便打印所有配置（可选）
    def __repr__(self):
        return (
            f"Config(\n"
            f"  BOT_TOKEN='{self.BOT_TOKEN}',\n"
            f"  DB_URL='{self.DB_URL}',\n"
            f"  PROXY='{self.PROXY}',\n"
            f"  OPEN_BASIC_URL='{self.OPEN_BASIC_URL}',\n"
            f"  OPEN_KEY='{self.OPEN_KEY}',\n"
            f"  MODEL_TYPE='{self.MODEL_TYPE}',\n"
            f"  SYSTEM_PROMPT='{self.SYSTEM_PROMPT}',\n"
            f"  ENV='{self.ENV}',\n"
            f"  LOG_LEVEL='{self.LOG_LEVEL}'\n"
            f")"
        )


# 使用示例
if __name__ == "__main__":
    config = Config()
    print(config)
