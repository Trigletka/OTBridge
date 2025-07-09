from flask import Flask, request
from create_bot import bot, dp, WEBHOOK_PATH
import asyncio
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

app = Flask(__name__)

@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    # Передаем данные из Flask → aiohttp handler
    loop = asyncio.get_event_loop()
    req_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    # Flask → aiohttp
    # создаем фейковый aiohttp request из flask request
    from aiohttp.web_request import BaseRequest
    from types import SimpleNamespace
    fake_request = SimpleNamespace(
        headers=request.headers,
        method=request.method,
        rel_url=request.url,
        query=request.args,
        read=lambda: request.get_data()
    )
    response = loop.run_until_complete(req_handler.handle(fake_request))
    return response.body, response.status, response.headers.items()
