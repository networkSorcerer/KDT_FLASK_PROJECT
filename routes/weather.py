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

# 위치정보를 받아서 해당 위치의 현재 온도, 습도, 강수량이 표시 되도록 수정

def get_short_term_weather():
    API_KEY = "LPh8U0fWWitEfCUYAQMCreTSbSbI4XqYB%2Bspk2jhS90QAcvAT1FforFEAfawd9rL4yV8Ecqs%2B0pv6G9eMYM5yA%3D%3D"
    API_KEY_DECODE = 'Va8g+wrI2rBylM2BYEtI2nMGQz0tlWWqvFNg6SiQlqZaMizJqW9jQ15LoKxKTXWaPCs7eqiADX3QMVswr8DMLQ=='

    # 현재 시간 가져오기
    now = datetime.datetime.now()

    # 서식에 맞게 날짜 정보 변경
    date = now.strftime('%Y%m%d')



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

    # 한페이지에 포함된 결과수
    num_of_rows = 6
    page_no = 1
    data_type = 'JSON'

    # params = {'serviceKey': '서비스키', 'pageNo': '1', 'numOfRows': '1000', 'dataType': 'XML', 'base_date': '20210628',
    #           'base_time': '0600', 'nx': '55', 'ny': '127'}

    req_parameter = {'serviceKey': API_KEY_DECODE,
                     'nx': nx_val, 'ny':ny_val,'base_date':baseDate, 'base_time':baseTime, 'pageNo':page_no,
                     'numOfRows':num_of_rows, "dataType":data_type}
    # 요청과 응답
    try:
        response = requests.get(url, params = req_parameter)
    except requests.exceptions.RequestException as e :
        print(f"날씨 정보 요청 실패 : {e}")
        return json.dumps({"에러": str(e)}, ensure_ascii=False)
    # JSON 형태로 응답 받은 데이터를 딕셔너리로 변환
    dict_data = response.json()

    # 출력을 이쁘게 하기 위해 json.dumps()를 사용하여 들여쓰기(indent) 옵션을 지정
    print(json.dumps(dict_data, indent=2))

    # 딕셔너리 데이터를 분석하여 원하는 데이터를 추출
    weather_items = dict_data['response']['body']['items']['item']

    print(f"[ 발표 날짜 : {weather_items[0]['baseDate']} ]")
    print(f"[ 발표 시간 : {weather_items[0]['baseTime']} ]")

    weather_data = {}

    for k in range(len(weather_items)):
        weather_item = weather_items[k]
        obsrValue = weather_item['obsrValue']
        if weather_item['category'] == 'T1H':
            weather_data['tmp'] = f"{obsrValue}℃"
        elif weather_item['category'] == 'REH':
            weather_data['hum'] = f"{obsrValue}%"
        elif weather_item['category'] == 'RN1':
            weather_data['pre'] = f"{obsrValue}mm"
    # 딕셔너리를 JSON 형태로 변환
    json_weather = json.dumps(weather_data, ensure_ascii=False, indent=4)
    return json_weather
