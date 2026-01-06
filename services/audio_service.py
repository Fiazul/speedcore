import subprocess
import os
import time
import random
from pathlib import Path
from core.config import TEMP_FOLDER, SARCASM_ERROR

class AudioProcessingError(Exception):
    """Custom exception for audio processing failures."""
    def __init__(self, message, sarcasm=None):
        super().__init__(message)
        self.sarcasm = sarcasm or random.choice(SARCASM_ERROR)

class AudioService:
    @staticmethod
    def download_audio(url: str) -> str:
        """Downloads audio from YouTube and returns the file path."""
        print(f"[AudioService] Downloading: {url}")
        
        # Check for cookies.txt in multiple locations
        cookies_paths = [
            os.path.join(os.getcwd(), 'cookies.txt'),           # App root
            '/etc/secrets/cookies.txt',                          # Render secret files
        ]
        
        cookies_path = None
        for path in cookies_paths:
            if os.path.exists(path):
                cookies_path = path
                break
        
        download_cmd = [
            'yt-dlp', 
            '-x', 
            '--audio-format', 'flac',
            '--audio-quality', '0',
            # Aggressive bot bypass (ios client is most reliable)
            '--extractor-args', 'youtube:player_client=ios,android_creator;player_skip=webpage,configs',
        ]

        # Use cookies if available
        if cookies_path:
            print(f"[AudioService] Using cookies from: {cookies_path}")
            download_cmd.extend(['--cookies', cookies_path])
        else:
            print("[AudioService] WARNING: No cookies.txt found. YouTube may block this request.")
            print("[AudioService] To fix: Export cookies from your browser and place cookies.txt in the project root.")
        
        download_cmd.extend([
            url,
            '-o', f'{TEMP_FOLDER}/%(title)s.%(ext)s',
            '--print', 'after_move:filepath',
            '--no-warnings'
        ])
        
        try:
            result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=300, check=False)
            
            if result.returncode != 0:
                raise AudioProcessingError(f"Download failed: {result.stderr}")
            
            stdout_lines = [line for line in result.stdout.strip().split('\n') if line.strip()]
            downloaded_file = stdout_lines[-1] if stdout_lines else ""
            
            if not downloaded_file or not os.path.exists(downloaded_file):
                raise AudioProcessingError("Downloaded file not found.")
                
            return downloaded_file
            
        except subprocess.TimeoutExpired:
            raise AudioProcessingError("Download timed out. Maybe your internet is still on dial-up?")
        except Exception as e:
            if isinstance(e, AudioProcessingError):
                raise e
            raise AudioProcessingError(str(e))

    @staticmethod
    def process_nightcore(input_path: str, params: dict) -> str:
        """Processes the audio file into nightcore using ffmpeg."""
        print(f"[AudioService] Processing: {input_path}")
        
        mode = params.get('mode', 'custom')
        format_ext = params.get('format', 'flac')
        
        if mode == 'vocalfree':
            audio_filter = 'pan=stereo|c0=c0-c1|c1=c1-c0,highpass=f=120,lowpass=f=16000'
        else:
            filter_parts = [f'asetrate=44100*{params["sampleRate"]}', 'aresample=44100']
            
            if params.get('tempo', 1.0) != 1.0:
                filter_parts.append(f'atempo={params["tempo"]}')
            
            if params.get('bassBoost', 0) != 0:
                filter_parts.append(f'equalizer=f=100:t=q:w=1:g={params["bassBoost"]}')
            if params.get('midBoost', 0) != 0:
                filter_parts.append(f'equalizer=f=3000:t=q:w=1:g={params["midBoost"]}')
            if params.get('trebleBoost', 0) != 0:
                filter_parts.append(f'equalizer=f=8000:t=q:w=1:g={params["trebleBoost"]}')
            
            audio_filter = ','.join(filter_parts)

        output_name = f"nightcore_{int(time.time())}.{format_ext}"
        output_path = os.path.join(TEMP_FOLDER, output_name)
        
        codec_opts = ['-c:a', 'libmp3lame', '-q:a', '0'] if format_ext == 'mp3' else ['-c:a', 'flac', '-compression_level', '8']
        
        ffmpeg_cmd = ['ffmpeg', '-y', '-i', input_path, '-filter:a', audio_filter] + codec_opts + [output_path]
        
        try:
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                raise AudioProcessingError(f"FFmpeg failed: {result.stderr}")
                
            if not os.path.exists(output_path):
                raise AudioProcessingError("Output file was not created.")
                
            return output_name
            
        except subprocess.TimeoutExpired:
            raise AudioProcessingError("Processing timed out. This song is probably too long for me to care.")
        finally:
            # We no longer cleanup the original file here as the user wants to keep it
            # The background service will eventually clean it up anyway
            pass
