
FROM python:3.9-slim AS builder


LABEL maintainer="Karolina Żurek"


WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.9-slim


LABEL maintainer="Karolina Żurek"


WORKDIR /app


COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .


EXPOSE 5000


HEALTHCHECK CMD curl --fail http://localhost:5000 || exit 1


CMD ["python", "app.py"]