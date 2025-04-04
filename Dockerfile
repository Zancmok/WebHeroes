FROM python:3.13-slim

WORKDIR /app

COPY ./src /app/src

COPY requirements.txt /app/

COPY .env /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000

CMD ["python", "/app/src/main.py"]
