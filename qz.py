#ppom.py

import requests
import os
import json
import time
import copy
from bs4 import BeautifulSoup
from datetime import datetime

import kakao

# 변수 선언
site_url = 'https://m.ppomppu.co.kr/new/'  # 사이트 URL
board_list = []
p_board_list = []
keyword ='막걸리'


# 사이트에 파라미터로 넘길 조건들, 키워드 추가시 +뒤에 키워드 추가
params = {
    'search_type': 'subject',
    'keyword': keyword
}

# 조건 추가하여 사이트 오픈
result_search = requests.get('https://m.ppomppu.co.kr/new/bbs_list.php?id=ppomppu&category=', params=params)
# print(result_search.url)

# 사이트 리스트 가져오는 함수
def f_get_list():
    if result_search.status_code == 200:
        html = result_search.text
        soup = BeautifulSoup(html, 'html.parser')
        times = soup.select('#wrap > div.ct > div.bbs > ul > li > a > div.thmb_N2 > ul > li.exp > time')
        titles = soup.select('#wrap > div.ct > div.bbs > ul > li > a > div.thmb_N2 > ul > li.title > span.cont')
        links = soup.select('a.list_b_01n')

        for i in range(0, len(titles), 1):
            board_list.append('작성시간: ' +times[i].text +'\n제목: ' +titles[i].text.strip() +'\n링크: ' +site_url+links[i]['href'])
    else:
        print(result_search.status_code)

while True:
    f_get_list()  # 게시글 크롤링
    access_token = kakao.f_reissue_token()  # 새로운 액세스 토큰을 발급 받음
    sms_list = list(set(board_list) - set(p_board_list))  # 이전 리스트와 비교하여 다른 값만 문자 보낼 리스트로 저장
    p_board_list = copy.deepcopy(board_list)  # 현재 게시글을 이전 게시글로 저장

     authorization_kakao.f_send_msg(access_token, '뽐뿌 결과\n'  +'키워드 : '+keyword + '\n현재 시간 {} 최신글은 총 {}개입니다.'.format(datetime.now().strftime('%H:%M:%S'),len(sms_list)))

    for i in range(0, len(sms_list), 1):
        kakao.f_send_msg(access_token, sms_list[i])

    board_list.clear()
    sms_list.clear()
    time.sleep(1800)  # 반복 주기