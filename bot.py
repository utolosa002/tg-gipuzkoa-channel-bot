import os
import requests
from telegram import Bot
import asyncio
import urllib.parse
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
    job_elements2= results.find_all("div", class_="col-12 col-md-6 col-lg-4 mb-3")
    albisteak=[]

  #  print(job_elements)
    for job_element in job_elements:
        albistea=[]
       # print(job_element)
        title_element = job_element.find("h3", class_="izfe-title")
        desk_element  = job_element.find("p", class_="izfe-ultimas-noticias-resumen-destacada")
        data_element  = job_element.find("p", class_="small izfe-semibold text-white m-0 mr-2")
        img_element   = job_element.find_all("source")
        if len(img_element) == 0:
            img_element   = job_element.find_all("img")
            albistea.append(img_element[0]['src'])
        else:
            albistea.append("https://gipuzkoa.eus/"+img_element[0]['srcset'])
        url_element   = title_element.find(href=True)
        new_datatime = datetime.strptime(data_element.text, '%Y/%m/%d')
        albistea.append(title_element.text.strip()+ "\n" + url_element['href'])
        albistea.append(new_datatime)
        albisteak.append(albistea)
        
    for job_element in job_elements2:
        albistea=[]
        title_element = job_element.find("h3", class_="izfe-h3")
        data_element  = job_element.find("p", class_="small izfe-semibold text-white m-0 mr-2")
        img_element   = job_element.find_all("source")
        if len(img_element) == 0:
            img_element   = job_element.find_all("img")
            albistea.append(img_element[0]['src'])
        else:
            albistea.append("https://gipuzkoa.eus/"+img_element[0]['srcset'])
        url_element   = title_element.find(href=True)
        new_datatime = datetime.strptime(data_element.text, '%Y/%m/%d')
        albistea.append(title_element.text.strip()+ "\n" + url_element['href'])
        albistea.append(new_datatime)
        albisteak.append(albistea)
    return albisteak
    

async def send_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def send_photo(photo, caption):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo, caption=caption)

async def main():
    albisteak = get_news()
    gaur = datetime.strftime(datetime.today(), '%Y/%m/%d')
    for albistea in albisteak:
        img = albistea[0]
        irudia=img.split('?')
        title= albistea[1]
        caption = f"{title}"
        new_datatime = albistea[2]
        albiste_data = datetime.strftime(new_datatime, '%Y/%m/%d')
        if albiste_data != gaur:
            print(gaur)
            print(albiste_data)
        else:
            await send_photo(irudia[0],caption)
   
if __name__ == '__main__':
    asyncio.run(main())
