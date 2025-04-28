
# Zadanie 1 – Aplikacja pogodowa w kontenerze Docker

---

##  Aplikacja pogodowa 
### Funkcjonalność

- Po uruchomieniu kontenera aplikacja zapisuje w logach:
  - datę i godzinę uruchomienia,
  - imię i nazwisko autora: **Karolina Żurek**,
  - numer portu TCP: **5000**.
- Aplikacja pozwala użytkownikowi:
  - wybrać kraj z listy (Poland, USA, Germany),
  - następnie wybrać miasto,
  - pobrać aktualną pogodę dla wybranego miasta (temperatura, opis pogody, wilgotność).

---

### Kod źródłowy

**app.py**
```python
from flask import Flask, render_template, request
import requests
import logging
from datetime import datetime

# Konfiguracja logowania
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
```

---

**templates/index.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>
</head>
<body>
    <h1>Weather App</h1>
    <form method="POST">
        <label for="country">Wybierz kraj:</label>
        <select name="country" id="country" onchange="this.form.submit()" required>
            <option value="">-- Wybierz kraj --</option>
            {% for country in locations.keys() %}
            <option value="{{ country }}" {% if selected_country == country %}selected{% endif %}>{{ country }}</option>
            {% endfor %}
        </select>

        <label for="city">Wybierz miasto:</label>
        <select name="city" id="city" required>
            <option value="">-- Wybierz miasto --</option>
            {% for city in cities %}
            <option value="{{ city }}" {% if selected_city == city %}selected{% endif %}>{{ city }}</option>
            {% endfor %}
        </select>

        <button type="submit">Pobierz pogodę</button>
    </form>

    {% if weather_info %}
    <h2>Informacje o pogodzie:</h2>
    <p>Temperatura: {{ weather_info.temperature }}°C</p>
    <p>Opis: {{ weather_info.description }}</p>
    <p>Wilgotność: {{ weather_info.humidity }}%</p>
    {% endif %}
</body>
</html>
```

---

**requirements.txt**
```
Flask
requests
```

---

## 2. Dockerfile

**Dockerfile**
```Dockerfile
FROM python:3.11-slim as builder
LABEL org.opencontainers.image.authors="Karolina Żurek"

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

FROM python:3.11-slim
LABEL org.opencontainers.image.authors="Karolina Żurek"

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . /app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s CMD curl -f http://localhost:5000 || exit 1

CMD ["python", "app.py"]
```

---

## 3. Polecenia Docker

### a) Budowanie obrazu
```bash
docker build -t weather-app2 .
```

### b) Uruchomienie kontenera
```bash
docker run -d -p 5000:5000 --name weather-container weather-app2
```

### c) Podgląd logów aplikacji
```bash
docker logs weather-container
```
![image](https://github.com/user-attachments/assets/3196d7d8-1c32-44ab-b0ad-f1ddf52fdedd)


### d) Sprawdzenie liczby warstw i rozmiaru obrazu
```bash
docker history weather-app2
docker image inspect weather-app2 --format='{{.Size}}'
```
![image](https://github.com/user-attachments/assets/4a7cbbda-ab2d-4090-83fd-40d93b5d6d14)
![image](https://github.com/user-attachments/assets/0fd147aa-af6a-4b88-9a95-9030fc3adaf0)

---

## 4. Zrzut ekranu działania aplikacji

![image](https://github.com/user-attachments/assets/d1949c7e-e4da-493a-bba2-ef94316da31e)

---


