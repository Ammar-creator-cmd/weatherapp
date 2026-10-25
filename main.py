import os #

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)
API_KEY = os.environ.get("OPENWEATHER_API_KEY")
API_URL = "https://api.openweathermap.org/data/2.5/weather"

def query_api(city):
    if not API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY environment variable is not set.")
    response = requests.get(
        API_URL,
        params={"q": city, "mode": "json", "units": "metric", "appid": API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
#
@app.route('/')
def index():
    resp = query_api('London')
    print(resp)
    city = resp['name']
    temp = resp['main']['temp']
    country = resp['sys']['country']
    weather = resp['weather'][0]['description']
    iconcode = resp['weather'][0]['icon']
    humidity = resp['main']['humidity']
    feels_like = resp['main']['feels_like']
    return render_template('index.html', city=city, temp=temp, country=country, weather=weather,
                           iconcode=iconcode, humidity=humidity, feels_like=feels_like)

@app.route("/results", methods=["GET", "POST"])
def result():
    input_city = request.form.get("city")
    resp = query_api(input_city)
    error = None
    if resp:
        if len(resp) <= 2:
            error = resp["message"]
        else:
            temp = resp["main"]["temp"]
            city = resp["name"]
            country = resp["sys"]["country"]
            weather = resp["weather"][0]["description"]
            iconcode = resp["weather"][0]["icon"]
            humidity = resp["main"]["humidity"]
            feels_like = resp["main"]["feels_like"]
            return render_template( "index.html", city=city, temp=temp, country=country, weather=weather, iconcode=iconcode, humidity=humidity, feels_like=feels_like)

    return render_template("index.html", error=error)
if __name__ == '__main__':
    app.run(debug=True)