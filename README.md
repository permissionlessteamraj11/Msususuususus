# PritiMusic 🎵

A premium-grade Telegram voice chat music bot system.

## Features
- Premium UI with Neon Orange theme
- Assistant + Bot architecture
- MongoDB Persistence
- YouTube & Spotify support
- Visual thumbnails and progress status
- Admin & User control panels
- Scalable and modular design

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create a `.env` file from `.env.example` and fill in the values.
4. Run the bot: `python3 main.py`.

## Deployment
### VPS
```bash
sudo apt update && sudo apt install ffmpeg -y
pip3 install -r requirements.txt
python3 main.py
```

### Render / Docker
Use the provided `render.yaml` or `Dockerfile`.
