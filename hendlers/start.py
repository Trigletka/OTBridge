import aiohttp
import io
import discord
from aiogram import Router
from aiogram.types import Message
from create_bot import bot, DISCORD_CHANNEL_ID, botDS

router = Router()


@router.message()
async def my_handler(message: Message) -> None:
    print(message)

@botDS.event
async def on_ready():
    print(f"Discord bot logged in as {botDS.user}")


@router.channel_post()
async def photo_or_video_handler(message: Message) -> None:
    file_id = None
    filename = None
    content_type = None
    if message.photo:
        file_id = message.photo[-1].file_id
        filename = "photo.jpg"
        content_type = "image/jpeg"
    elif message.video:
        file_id = message.video.file_id
        filename = "video.mp4"
    elif message.animation:
        file_id = message.animation.file_id
        filename = "animation.gif"
        content_type = "image/gif"
    elif message.document:
        mime = message.document.mime_type
        if mime == "image/gif":
            file_id = message.document.file_id
            filename = message.document.file_name or "document.gif"
            content_type = "image/gif"
    else:
        return

    file = await bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"
    print(file_url)

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            if resp.status != 200:
                print("Ошибка загрузки медиа из Telegram")
                return
            file_bytes = await resp.read()

            buffer = io.BytesIO(file_bytes)
            buffer.seek(0)

    discord_file = discord.File(buffer, filename=filename) #ds file

    caption = message.caption if message.caption else ""

    channel = botDS.get_channel(DISCORD_CHANNEL_ID)
    await channel.send(content=caption, file=discord_file)