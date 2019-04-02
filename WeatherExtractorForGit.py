# OpenWeatherMap の API を利用してその日の気温を取得する

# OpenWeatherMap API Tutorial Page
# https://agromonitoring.com/api/get

# PyDrive での対象ファイルは Root > PythonWorks > Git > WeatherExtractor

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import urllib.request as req
import xml.etree.ElementTree as et

import datetime
import csv


def auth_google():
    # Google Oauth 認証を行う
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile('credentials.json')
    if gauth.credentials is None:
        # Authenticate if they're not there
        # gauth.LocalWebserverAuth()
        gauth.CommandLineAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile('credentials.json')

    drive = GoogleDrive(gauth)

    """
    # Git > WeatherExtractor 内のファイル一覧を ID と共に表示
    drive_folder_id = '1X_lNjACsoUWbnz3Y-PSoP5e4hplV_f4d'
    query = '"{0}" in parents and trashed=false'.format(drive_folder_id)
    file_list = drive.ListFile({'q': query}).GetList()
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
        print(file1)
    """

    # WeatherResult.csv を操作してみる
    # drive_csv_id = '1sCCMDIAMfHTt013R28lVxQj31VlgMopV'
    # file = drive.CreateFile({'id': drive_csv_id})
    # file = drive.CreateFile({'title': 'a.csv',
    #                          'parents': [{'id': '1X_lNjACsoUWbnz3Y-PSoP5e4hplV_f4d'}]})
    drive_folder_id = '1X_lNjACsoUWbnz3Y-PSoP5e4hplV_f4d'
    query = '"{0}" in parents and trashed=false'.format(drive_folder_id)
    file_list = drive.ListFile({'q': query}).GetList()
    for file in file_list:
        if file['title'] == 'WeatherResult.csv':  # WeatherResult.csv を取得してダウンロードする
            content = file.GetContentString()
            file2 = file
            # print(file2)
            break
    # print(content)
    # print(type(content))
    file2.GetContentFile('a.csv')  # csv ファイルとしてダウンロード
    file2.Trash()  # WeatherResult.csv をゴミ箱に移動
    file2.UnTrash()  # ゴミ箱の外に移動?
    file2.Delete()  # Hard Delete
    # file.GetContentFile('a.txt')

    return drive


def write_csv():
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
    day = dt_now.day

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
    with open('a.csv', mode='a', newline='') as f:
        writer = csv.writer(f)
        # writer.writerow([present_date, present_time, last_update_time, sunrise, sunset, temperature, humidity, pressure, weather])
        writer.writerow([year, month, day, present_time, last_update_time, sunrise, sunset, temperature, humidity, pressure, weather])

    print('DONE')
    print('Present Day: {0}'.format(present_date))
    print('Present Time: {0}'.format(present_time))
    print('Present Temperature: {0}'.format(temperature))


def upload_file(drive):
    # PythonWorks > Git > WeatherExtractor のフォルダ ID
    file2 = drive.CreateFile({'parents': [{'id': '1X_lNjACsoUWbnz3Y-PSoP5e4hplV_f4d'}]})
    file2.SetContentFile('a.csv')
    file2['title'] = 'WeatherResult.csv'
    file2.Upload()


if __name__ == '__main__':
    drive = auth_google()
    write_csv()
    upload_file(drive=drive)