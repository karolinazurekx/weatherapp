# Etap 1: Budowanie aplikacji
FROM python:3.9-slim AS builder

# Informacja o autorze
LABEL maintainer="Karolina Żurek"

# Instalacja zależności
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Etap 2: Finalny obraz
FROM python:3.9-slim

# Informacja o autorze
LABEL maintainer="Karolina Żurek"

# Ustawienia aplikacji
WORKDIR /app

# Kopiowanie zależności i aplikacji
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .

# Ekspozycja portu
EXPOSE 5000

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:5000 || exit 1

# Uruchamianie aplikacji
CMD ["python", "app.py"]