#kakao.py

import time
import requests
import json

with open('kakaoid', 'r') as f:
    secret = {l.split('=')[0]: l.split('=')[1].rstrip() for l in f.readlines()}

# code url  https://kauth.kakao.com/oauth/authorize?client_id=자신의 rest api key 값&redirect_uri=https://example.com/oauth&response_type=code
url = 'https://kauth.kakao.com/oauth/token'  # 카톡 인증 url
# rest_api_key = '자신의 rest api key 값'  # 카톡 rest 키
rest_api_key = secret['rest_api_key']
redirect_uri = 'https://example.com/oauth'  # 카톡 인증용 redirect url
authorize_code = 'code url을 통해 얻은 code 값'  # 카톡 인증용 코드 수행시마다 재발급 필요


# 최초 token들 발급하여 refresh token 저장
def f_get_refresh_token():
    data = {
        'grant_type': 'authorization_code',
        'client_id': rest_api_key,
        'redirect_uri': redirect_uri,
        'code': authorize_code,
    }

    response = requests.post(url, data=data)
    tokens = response.json()

    with open('refresh_token.json', 'w') as fd:
        json.dump(tokens, fd)


# refresh token을 이용하여 새로운 access token 발급
def f_reissue_token():
    with open('refresh_token.json', 'r') as fd:
        token = json.load(fd)
    refresh_token = token['refresh_token']
    data = {
        'grant_type': 'refresh_token',
        'client_id': rest_api_key,
        'refresh_token': refresh_token
    }
    response = requests.post(url, data=data)
    tokens = response.json()

    with open('access_token.json', 'w') as fd:
        json.dump(tokens, fd)
    with open('access_token.json', 'r') as fd:
        ts = json.load(fd)
    access_token = ts['access_token']
    return access_token


# 메시지 전송
def f_send_msg(access_token, msg):
    header = {'Authorization': 'Bearer ' + access_token}
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'  # 나에게 보내기 주소
    post = {
        'object_type': 'text',
        'text': msg,
        'link': {
            'web_url': 'https://developers.kakao.com',
            'mobile_web_url': 'https://developers.kakao.com'
        },
        'button_title': '키워드'
    }
    data = {'template_object': json.dumps(post)}
    return requests.post(url, headers=header, data=data)