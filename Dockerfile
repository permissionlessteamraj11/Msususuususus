FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
