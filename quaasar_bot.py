import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import os
import telegram
import asyncio

# 토큰 아이디 가져오기
def get_id():
    with open('snsid', 'r') as f:
        secret = {l.split('=')[0]: l.split('=')[1].rstrip() for l in f.readlines()}

    token = secret['telegram_token']
    test1id = secret['test1id']
    return token, test1id

# 크롤링 함수
def gethotdeal():
    op = webdriver.ChromeOptions()
    op.add_argument("headless")
    op.add_argument('user-agent=Mozilla/5.0')
    driver = webdriver.Chrome('./chromedriver.exe', options=op)
    driver.get('https://quasarzone.com/bbs/qb_saleinfo')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 링크, 제목, 쇼핑몰, 가격, 작성시간, 고유키
    # 링크
    table = soup.find("table")
    #print(table)
    post = table.find("a", class_="subject-link")["href"]
    #print(post)
    posts = 'https://quasarzone.com'+ post

    # 제목, 쇼핑몰
    tit = soup.select(".ellipsis-with-reply-cnt")[0].text
    mall, title = tit.split(']')[0][1:], tit.split(']')[1] 

    # 가격
    price = soup.select(".text-orange")[0].text

    # 작성시간
    date = soup.select(".date")[0].text.strip()

    latest = posts + '\t' + title + '\t' + mall + price + '\t' + date

    return latest

# 메세지 부분
def send_tgmessage(latest, key_word):
    token, test1id= get_id()
    BASE_DIR = os.path.dirname(os.path.abspath('__file__'))
    async def main(hotdealmessage): #실행시킬 함수명 임의지정
        token = token
        chat_id= test1id
        bot = telegram.Bot(token = token)
        await bot.send_message(chat_id, hotdealmessage)


    with open(os.path.join(BASE_DIR, 'quasar_zone.txt'), 'r+') as f_read:
        before = f_read.readline()
        #if (before != latest):
        if (before != latest) & (key_word in latest):
            hotdealmessage = f'{key_word} 관련 새 글이 올라왔어요!' +  latest # posts
            asyncio.run(main(hotdealmessage))
            print('전송했음')
        else: 
            pass
        f_read.close()

    with open(os.path.join(BASE_DIR, 'quasar_zone.txt'), 'w+') as f_write:
        f_write.write(latest)
        f_write.close()

# while 1==1:
#     send_tgmessage(gethotdeal(), '990 pro')
#     time.sleep(90)