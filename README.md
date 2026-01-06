# 🎵 Musica: The Sarcastic Nightcore Generator

Welcome to **Musica**. I'll turn your favorite songs into high-pitched experiments. Are you happy now?

## 🚀 Features
- **Fast Nightcore**: Powered by `ffmpeg`. It's faster than you downloading suspicious `.exe` files from 2012.
- **YouTube Support**: Give me a URL, and I'll do the rest. (Unless the URL is broken, which it probably is).
- **Premium UI**: Dark mode, glassmorphism, and subtle micro-animations. Because if it doesn't look good, why bother?
- **Sarcastic Personality**: I'll judge your taste in music and complain about the work I'm doing.
- **Modular Design**: Clean, separated code for people who actually care about how things are built.
- **Auto-Cleanup**: I delete your files after 10 minutes. I'm not your storage provider.

## ⚠️ Beta Warning: Vocal Free
The **Vocal Free** feature is in **Alpha/Beta**. It uses phase cancellation (karaoke effect) to try and remove vocals. 
- It might mess up your audio.
- it might not work at all for some songs.
- It might just sound weird.
Don't come crying to me if it doesn't work.

## 🛠️ Tech Stack
- **FastAPI**: For the backend speed.
- **yt-dlp**: For grabbing audio from the tubes.
- **ffmpeg**: For the heavy lifting of audio processing.
- **Vanilla CSS**: For that custom premium feel without the bloat.

## 📦 Installation

1. **Clone this repository** (If you know how to use git).
2. **Install system dependencies**:
   ```bash
   sudo apt update && sudo apt install ffmpeg
   ```
3. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Running Locally

```bash
uvicorn main:app --reload
```
Then visit `http://localhost:8000`. Good luck.

## 📂 Project Structure
```text
.
├── api/            # Pydantic models and API routes
├── core/           # Configuration and settings
├── services/       # Audio processing and cleanup logic
├── templates/       # The pretty UI
├── main.py         # The entry point
└── README.md       # This file. Read it.
```

## 📄 License
MIT. Use it, break it, whatever. Just don't blame me.
