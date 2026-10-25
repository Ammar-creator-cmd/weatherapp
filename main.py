import os

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


def render_weather(city):
    if not city:
        return render_template("index.html", error="Please enter a city name.")

    try:
        weather = query_api(city)
    except RuntimeError as exc:
        return render_template("index.html", error=str(exc), searched_city=city)
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            error = f"Could not find weather for {city}. Check the spelling and try again."
        else:
            error = "The weather service returned an error. Please try again later."
        return render_template("index.html", error=error, searched_city=city)
    except requests.RequestException:
        return render_template(
            "index.html",
            error="Could not reach the weather service. Please try again later.",
            searched_city=city,
        )

    current = weather["main"]
    return render_template(
        "index.html",
        city=weather["name"],
        country=weather["sys"]["country"],
        temp=current["temp"],
        temp_max=current["temp_max"],
        temp_min=current["temp_min"],
        feels_like=current["feels_like"],
        weather=weather["weather"][0]["description"],
        iconcode=weather["weather"][0]["icon"],
        longitude=weather["coord"]["lon"],
        latitude=weather["coord"]["lat"],
        humidity=current["humidity"],
        pressure=current["pressure"],
        windspeed=weather["wind"]["speed"],
        searched_city=city,
    )


@app.route("/")
def index():
    return render_weather("London")


@app.route("/results", methods=["POST"])
def result():
    input_city = request.form.get("city", "").strip()
    return render_weather(input_city)


if __name__ == "__main__":
    app.run(debug=True)