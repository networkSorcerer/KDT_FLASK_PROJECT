import json # JSON 직렬화 / 역직렬화
import requests # http 통신
from bs4 import BeautifulSoup
from flask import request
import datetime

def get_sample_weather():
    url = "http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108"
    # HTTP GET 요청
    response = requests.get(url)
    # HTMP Parsing
    soup = BeautifulSoup(response.text, "html.parser")
    html_output=""
    for loc in soup.select("location"):
        html_output += f"<h2>{loc.select_one('city').string}</h2>"
        html_output += f"<h4>날씨 : {loc.select_one('wf').string}</h4>"
        html_output += f"<h4>최저 / 최고 기온 : {loc.select_one('tmn')}/{loc.select_one('tmx')}</h4>"
        html_output += "</hr>"
    return html_output

def get_short_term_weather():
    API_KEY = "LPh8U0fWWitEfCUYAQMCreTSbSbI4XqYB%2Bspk2jhS90QAcvAT1FforFEAfawd9rL4yV8Ecqs%2B0pv6G9eMYM5yA%3D%3D"
    API_KEY_DECODE = requests.utils.unquote_unreserved(API_KEY)

    # 현재 시간 가져오기
    now = datetime.datetime.now()

    # 서식에 맞게 날짜 정보 변경
    date = now.strftime('%Y%m%d')

    # 서식에 맞게 시간 정보 변경
    time = now.strftime('%H%M')

    # 현재 분이 30분 이전이면 30분 전 시간으로 설정
    if now.minute < 30:
        now = now - datetime.timedelta(minutes=30)
        time = now.strftime('%H%M')
    else:
        time = now.strftime('%H%M')

    # 요청 주소
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'

    #요청 일자 지정
    baseDate = date
    baseTime = time

    # 예보 지점 (서울시 강남구 역삼동)
    nx_val = 62
    ny_val = 126

