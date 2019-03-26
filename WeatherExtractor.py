#
# OpenWeatherMap の API を利用してその日の気温を取得する

# OpenWeatherMap API Tutorial Page
# https://agromonitoring.com/api/get

import urllib.request as req

import xml.etree.ElementTree as et
import xml.dom.minidom as md

import datetime
import csv

city_name = 'Fukuoka'
# 自分のアカウントの API Key を指定
api_key = 'b06df852c216e1ac8aaab680be33d554'
mode = 'xml'
units = 'metric'

api = 'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}&mode={mode}&units={units}'
# リクエストURL のキーを入力
url = api.format(city=city_name, key=api_key, mode=mode, units=units)

# http リクエスト
response = req.urlopen(url)
data = response.read()
text = data.decode('utf-8')

# 取得したコンテンツをXML Element に格納
root = et.fromstring(text)
# minidom モジュールが XML Element をパース
# document = md.parseString(et.tostring(root, 'utf-8'))
# パースされたXML情報をインデント付きで文字列に変換して表示
# print(document.toprettyxml(indent='  '))

e = root.find('lastupdate')
lastupdate = e.get('value')

e = root.find('city')
e = e.find('sun')
sunrise = e.get('rise')
sunset = e.get('set')

e = root.find('temperature')
temperature = e.get('value')

e = root.find('humidity')
humidity = e.get('value')

e = root.find('pressure')
pressure = e.get('value')

e = root.find('weather')
weather = e.get('value')

# 現在の時間を取得
dt_now = datetime.datetime.now()
present_date = dt_now.date()
present_time = dt_now.time()
year = dt_now.year
month = dt_now.month
date = dt_now.day

# lastupdate, sunrise_time, sunset_time を UTC -> JST に変更
td_9h = datetime.timedelta(hours=9)  # 9時間分の timedelta オブジェクト
last_update_time = datetime.datetime.strptime(lastupdate, '%Y-%m-%d'+'T'+'%H:%M:%S')
last_update_time += td_9h
last_update_time = datetime.time(last_update_time.hour, last_update_time.minute, last_update_time.second)
sunrise = datetime.datetime.strptime(sunrise, '%Y-%m-%d'+'T'+'%H:%M:%S')
sunrise += td_9h
sunrise = datetime.time(sunrise.hour, sunrise.minute, sunrise.second)
sunset = datetime.datetime.strptime(sunset, '%Y-%m-%d'+'T'+'%H:%M:%S')
sunset += td_9h
sunset = datetime.time(sunset.hour, sunset.minute, sunset.second)

# 書き込み
with open('TestWeather.csv', mode='a') as f:
    writer = csv.writer(f)
    writer.writerow([present_date, present_time, last_update_time, sunrise, sunset, temperature, humidity, pressure,
                     weather])








