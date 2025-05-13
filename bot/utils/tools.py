import gettext
import os


def get_translator(lang_code: str):
    """
    加载翻译
    :param lang_code: 目标语言代码，例如 'en' 或 'zh'
    :return: 翻译函数
    """
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        localedir = os.path.join(base_dir, "locales")
        return gettext.translation('messages', localedir=localedir, languages=[lang_code], fallback=True).gettext
    except FileNotFoundError:
        print(f"Translation files for {lang_code} not found!")
        return gettext.gettext  # 返回默认翻译函数（即不做翻译）


if __name__ == '__main__':
    def main():
        # 测试不同语言的翻译
        lang_code = 'en'  # 可以切换为 'en' 或 'zh'
        _ = get_translator(lang_code)

        # 测试翻译
        print(_("开始"))  # 期望输出 "你好"（对于 zh）或 "Hello"（对于 en）
        print(_("语言设置"))  # 期望输出 "再见"（对于 zh）或 "Goodbye"（对于 en）


    main()
