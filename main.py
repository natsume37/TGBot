import asyncio
from bot.bot import main
from compile_translations import compile_mo_files

if __name__ == '__main__':
    # compile_mo_files()
    asyncio.run(main())
