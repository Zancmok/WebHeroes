FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    liblua5.4 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["sh", "-c", "python main.py"]
