# 📡 DX-Spot Discord-Bot

Ein einfacher Discord-Bot, der auf Anfrage die **10 aktuellsten DX-Spots** per Slash-Befehl (`/dxspots`) als Discord-Embed-Nachrichten ausgibt.

---

## 🚀 Features

- ✅ Slash-Befehl `/dxspots`
- 📶 Zeigt 10 aktuelle DX-Spots
- 🌐 Abruf über öffentliche API: [`web.cluster.iz3mez.it`](https://web.cluster.iz3mez.it/spots.json/)
- 🕓 Zeitanzeige in UTC
- 🇩🇪 Ausgabe auf Deutsch
- 🙋‍♂️ Powered by Patrick Weyand

---

## 🛠️ Voraussetzungen

- Python 3.8+
- Bot bei Discord registriert
- Channel-ID des Ziel-Discord-Channels

---

## 📦 Installation

```bash
git clone https://github.com/dein-benutzername/dxspot-discord-bot.git
cd dxspot-discord-bot
pip install -r requirements.txt


📸 Beispielausgabe

🌐 DX Spot: K1ABC
📡 Frequenz: 14.074 MHz
📶 Band: 20m
👤 Spotter: DL7XYZ
🕓 Zeit (UTC): 2025-08-06T09:35:12
📢 Powered by Patrick Weyand
