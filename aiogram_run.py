import logging
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from create_bot import bot, dp, BASE_URL, WEBHOOK_PATH, HOST, PORT, ADMIN_ID, botDS, DS_TOKEN
from hendlers.start import router
import asyncio


# меню
async def set_commands():
    commands_tg = [BotCommand(command='start', description='Старт')]
    await bot.set_my_commands(commands_tg, BotCommandScopeDefault())


# Функция при запуске
async def on_startup() -> None:
    await set_commands()
    await bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")
    await bot.send_message(chat_id=ADMIN_ID, text='Бот запущен!')


# остановка
async def on_shutdown() -> None:
    await bot.send_message(chat_id=ADMIN_ID, text='Бот остановлен!')
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()

async def start_telegram():
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=HOST, port=PORT)
    await site.start()

    logging.info("Telegram webhook server started.")

    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await on_shutdown()
        await runner.cleanup()
        
# запуск
async def main():
    telegram_task = asyncio.create_task(start_telegram())
    discord_task = asyncio.create_task(botDS.start(DS_TOKEN))

    await asyncio.gather(telegram_task, discord_task)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    asyncio.run(main())
