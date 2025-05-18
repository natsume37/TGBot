# compile_translations.py
import os
import polib
from pathlib import Path

import logging

logger = logging.getLogger(__name__)


def find_locales_dirs(root_dir: Path):
    """
    在 root_dir 及其子目录中查找所有名为 'locales' 的文件夹。
    返回一个 Path 列表。
    """
    return [p for p in root_dir.rglob('locales') if p.is_dir()]


def compile_mo_files():
    # 脚本所在目录
    script_dir = Path(__file__).resolve().parent

    # 查找所有 locales 目录
    locales_dirs = find_locales_dirs(script_dir)
    if not locales_dirs:
        logger.info(f"❌ 在 {script_dir} 及子目录中未找到任何 'locales' 文件夹。")
        return

    # 逐个处理每个 locales 目录
    for locale_dir in locales_dirs:
        logger.info(f"\n🔍 开始扫描：{locale_dir}")
        for root, dirs, files in os.walk(locale_dir):
            po_files = [f for f in files if f.endswith('.po')]
            if not po_files:
                continue
            for po_filename in po_files:
                po_path = Path(root) / po_filename
                mo_path = po_path.with_suffix('.mo')
                try:
                    logger.info(f"   ▶ 编译 {po_filename} …")
                    po = polib.pofile(str(po_path))
                    po.save_as_mofile(str(mo_path))
                    logger.info(f"   ✅ 成功：{mo_path.name}")
                except Exception as e:
                    logger.info(f"   ❌ 失败：{po_filename}，错误：{e}")

    logger.info("\n🎉 所有翻译已编译完毕！")


if __name__ == '__main__':
    compile_mo_files()
