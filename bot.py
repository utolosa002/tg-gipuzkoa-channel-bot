import os
import requests
from telegram import Bot
import asyncio
import hmac
import base64
import time
import urllib.parse
from hashlib import sha256

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_datuak():
    url = f'http://tiñelu.eus'
    response = requests.get(url)
    datuak_report = "Unable to fetch datuak data at the moment."
    return {'text': datuak_report}

async def send_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    print(response)

async def send_photo(photo, caption):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo, caption=caption)

async def main():
    datuak = get_datuak()
    message = f"{datuak}\n"
    await send_message(message)

if __name__ == '__main__':
    asyncio.run(main())