from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config
from discord import Intents
from discord.ext import commands

ADMIN_ID = int(config('ADMIN_ID'))
BOT_TOKEN = config("BOT_TOKEN")
HOST = config("HOST")
PORT = int(config("PORT"))
WEBHOOK_PATH = f'/{BOT_TOKEN}'
BASE_URL = config("BASE_URL")
DISCORD_CHANNEL_ID = int(config("DS_ID"))
DS_TOKEN = config("DS_TOKEN")

intents = Intents.default()
intents.message_content = True
botDS = commands.Bot(command_prefix='>', intents=intents)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()