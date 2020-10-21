import requests as req
import re
import demjson
import time

BASE_URL_FORMAT1 = 'http://tianqi.2345.com/t/wea_history/js/54857_{date}.js'
BASE_URL_FORMAT2 = 'http://tianqi.2345.com/t/wea_history/js/{date}/54857_{date}.js'

PATTERN = re.compile(r'{.*}')

def fetch_by_date(date, url):
    print(f'fetch ===> date={date}')
    resp = req.get(url)

    matched_str = re.search(PATTERN, resp.text).group()
    weathers = demjson.decode(matched_str)

    ret = []

    for weather_of_day in weathers.get('tqInfo'):
        if len(weather_of_day.items()) == 0:
            continue
        date = weather_of_day.get('ymd')
        max_t = weather_of_day.get('bWendu')
        min_t = weather_of_day.get('yWendu')
        weather = weather_of_day.get('tianqi')
        wind_direction = weather_of_day.get('fengxiang')
        wind_level = weather_of_day.get('fengli')

        aqi = weather_of_day.get('aqi', '')
        aqi_info = weather_of_day.get('aqiInfo', '')
        aqi_level = weather_of_day.get('aqiLevel', '')
        print(date, max_t, min_t, weather, wind_direction, wind_level, aqi, aqi_info, aqi_level)
        ret.append([date, max_t, min_t, weather, wind_direction, wind_level, aqi, aqi_info, aqi_level])
    return ret

def main():
    file = open('temparue.csv', 'w', encoding='GB2312')
    file.write(','.join(['日期', '最高温度', '最低温度', '天气', '风向', '风级', 'aqi', '空气质量', '空气质量等级'])+'\n')
    
    date_list = []
    url_list = []
for year in range(14, 20+1):
        end = False    
        for moth in range (1, 12+1):
            if year == 20 and moth == 6:
                end = True
                break 

            if year < 17:
                date = f'20{year}{moth}'
                url_list.append(BASE_URL_FORMAT1.format(date=date))
            else:
                date = f'20{year}{moth if moth >= 10 else "0" + str(moth)}'
                url_list.append(BASE_URL_FORMAT2.format(date=date))
            date_list.append(date)

        if end == True:
            break
        
    for date, url in zip(date_list, url_list):
        success = False
        while(not success):
            try:
                ret_list = fetch_by_date(date, url)
                for item in ret_list:
                    file.write(','.join(item)+'\n')
                success = True
            except Exception as e:
                print(e)
                time.sleep(1)
                pass
       
    


if __name__ == "__main__":
    main()