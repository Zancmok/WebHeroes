FROM python:3.13-slim

LABEL authors="Zancmok, immanis70"
LABEL title="Web Heroes"
LABEL version="0.0.1"

WORKDIR /app

COPY ./src /app/src

COPY requirements.txt /app/

COPY .env /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000

ENV PYTHONPATH="/app/src:${PYTHONPATH}"

CMD ["python", "/app/src/main.py"]
