from flask import Flask, render_template, request
import requests
import logging
from datetime import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


AUTHOR = "Karolina Żurek"
PORT = 5000


app = Flask(__name__)


API_KEY = "3e0d5569920c03e5fb6f86d3d9775e39"


LOCATIONS = {
    "Poland": ["Warsaw", "Krakow", "Gdansk"],
    "USA": ["New York", "Los Angeles", "Chicago"],
    "Germany": ["Berlin", "Munich", "Hamburg"]
}


logger.info(f"Application started on {datetime.now()}")
logger.info(f"Author: {AUTHOR}")
logger.info(f"Listening on TCP port: {PORT}")

@app.route("/", methods=["GET", "POST"])
def index():
    weather_info = None
    selected_country = None
    selected_city = None
    cities = []

    if request.method == "POST":
        selected_country = request.form.get("country")
        selected_city = request.form.get("city")

        
        if selected_country in LOCATIONS:
            cities = LOCATIONS[selected_country]

        
        if selected_country and selected_city:
            weather_info = get_weather(selected_city)

    return render_template("index.html", locations=LOCATIONS, cities=cities, weather_info=weather_info, selected_country=selected_country, selected_city=selected_city)

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=pl"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }
    return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)