import requests as r
from bs4 import BeautifulSoup as bs
import ast

# 気象庁api
weather_api = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"

# スクレイピング
rs = r.get(weather_api)
sp = bs(rs.text, "html.parser")

# 抽出
weather_dict = ast.literal_eval(str(sp))[0]

# 発表機関
publishingOffice = weather_dict["publishingOffice"]

# 発表時間
reported_time = weather_dict["reportDatetime"]

year = reported_time[0:4]
month = reported_time[5:7]
date = reported_time[8:10]
hour = reported_time[11:13]
minute = reported_time[14:16]

Time = "{}年{}月{}日 {}時{}分".format(year, month, date, hour, minute)

# 今日の天気の概要
todays_weather = weather_dict["timeSeries"][0]["areas"][0]["weathers"][0].replace("　", "")

# 気温
temps = weather_dict["timeSeries"][2]["areas"][0]["temps"]

lower_temp = temps[0]
upper_temp = temps[1]


# 送信

# トークンの読み込み
with open("token.txt", "r") as f:
    line_notify_token = f.read()
     
line_notify_api = 'https://notify-api.line.me/api/notify'

headers = {'Authorization': f'Bearer {line_notify_token}'}
message = f"\n{todays_weather}\n最低気温は{lower_temp}℃, 最高気温は{upper_temp}℃\n\n{Time} {publishingOffice}発表"
data = {'message': message}

r.post(line_notify_api, headers = headers, data = data)