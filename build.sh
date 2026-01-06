#!/usr/bin/env bash

# Exit on error
set -o errexit

echo "🚀 Starting build process..."

# 1. Install Python dependencies
echo "📦 Installing Python requirements..."
pip install -r requirements.txt
pip install yt-dlp

# 2. Check for ffmpeg (System dependency)
if ! command -v ffmpeg &> /dev/null
then
    echo "⚠️ ffmpeg not found. Attempting to install..."
    # This works on Render and Debian-based systems
    if [ "$RENDER" = "true" ] || [ "$(id -u)" -eq 0 ]; then
        apt-get update && apt-get install -y ffmpeg
    else
        echo "❌ Error: ffmpeg is not installed and I don't have sudo permissions."
        echo "Please run: sudo apt-get update && sudo apt-get install -y ffmpeg"
        exit 1
    fi
else
    echo "✅ ffmpeg is already installed."
fi

echo "✨ Build complete. You're ready to disappoint your ears."