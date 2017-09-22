import requests
import json
from flask import Flask, request, render_template

app = Flask(__name__)
history_list = []


def fetchWeather(input_words):
    result = requests.get('https://api.seniverse.com/v3/weather/now.json', params={
        'key': '4r9bergjetiv1tsd',
        'location': input_words,
        'language': 'zh-Hans',
        'unit': 'c'
    }, timeout=30)  # 请求的延时设置
    r = json.loads(result.text)  # json.loads() 将json格式转化为py数据格式
    city = r['results'][0]['location']['name']
    weather = r['results'][0]['now']['text']
    temperature = r['results'][0]['now']['temperature']
    search_time = r['results'][0]['last_update']
    search_result = "城市：{0}，天气：{1}，气温：{2} 摄氏度，查询时间：{3}".format(
        city, weather, temperature, search_time)
    return search_result


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/input_words')
def layout():
    if request.args.get('help') == "帮助":
        return render_template('help.html')

    elif request.args.get('history') == "历史":
        return render_template('history.html', history_list=history_list)

    elif request.args.get('search') == "查询":
        city = request.args.get('city')
        try:
            search_result = fetchWeather(city)
            history_list.append(search_result)
            return render_template('layout.html', search_result=search_result)
        except KeyError:
            return render_template('page_error.html')


if __name__ == '__main__':
    app.run(debug=True)


