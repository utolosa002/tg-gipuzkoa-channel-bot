import os
import requests
from telegram import Bot
import asyncio
import hmac
import base64
import time
import urllib.parse
from hashlib import sha256
from bs4 import BeautifulSoup
from datetime import * 

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_news():
    url = f'https://www.gipuzkoa.eus/eu/aktualitatea'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id="actualidad-ultimasnoticias")
    job_elements = results.find_all("div", class_="col-12 col-md-6 col-lg-12 mb-5")
    for job_element in job_elements:
        title_element = job_element.find("h3", class_="izfe-title")
        desk_element  = job_element.find("p", class_="izfe-ultimas-noticias-resumen-destacada")
        data_element  = job_element.find("p", class_="small izfe-semibold text-white m-0 mr-2")
        img_element   = job_element.find_all("img")
        url_element   = job_element.find_all(href=True)
        new_datatime = datetime.strptime(data_element.text, '%Y/%m/%d')
    return img_element[0]['src'], title_element.text.strip()+ "\n" + url_element[1]['href'], new_datatime

    

async def send_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def send_photo(photo, caption):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo, caption=caption)

async def main():
    img,title,new_datatime = get_news()
    caption = f"{title}"
    if new_datatime < datetime.today():
        exit
    else:
        await send_photo(img,caption)
   
if __name__ == '__main__':
    asyncio.run(main())