# Basis-Image mit Python 3.12 slim
FROM python:3.12-slim

# Systemabhängigkeiten (ffmpeg, Build Tools für PyNaCl)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis setzen
WORKDIR /app

# requirements.txt kopieren und Dependencies installieren
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Bot-Code kopieren
COPY . .

# Startbefehl
CMD ["python", "bot.py"]
