from flask import Flask, render_template, request
app = Flask(__name__)
import requests
API_KEY = ''
API_URL = ('http://api.openweathermap.org/data/2.5/weather?q={}&mode=json&units=metric&appid={}')

def query_api(city):
    print(API_URL.format(city, API_KEY))
    data = requests.get(API_URL.format(city, API_KEY)).json()
    return data

@app.route('/')
def index():
    city = "amsterdam"
    resp = query_api(city)
    print(resp)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)