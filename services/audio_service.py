import yt_dlp
import os
import time
import subprocess
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
        """Downloads audio from YouTube using yt-dlp library."""
        print(f"[AudioService] Downloading: {url}")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{TEMP_FOLDER}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'flac',
                'preferredquality': '0',
            }],
            'quiet': True,
            'no_warnings': True,
            # 'cookiefile': 'cookies.txt',  # Uncomment if you have a cookies file
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # The filename logic in yt-dlp is complex due to post-processing
                # We need to find the final .flac file
                if 'requested_downloads' in info:
                     filepath = info['requested_downloads'][0]['filepath']
                else:
                    # Fallback for when extract_info returns the info dict directly
                    filename = ydl.prepare_filename(info)
                    filepath = os.path.splitext(filename)[0] + ".flac"
                
                if not os.path.exists(filepath):
                     raise AudioProcessingError("Downloaded file disappeared into the void.")
                
                print(f"[AudioService] Downloaded to: {filepath}")
                return filepath

        except yt_dlp.utils.DownloadError as e:
            raise AudioProcessingError(f"Download failed: {str(e)}")
        except Exception as e:
            print(f"[AudioService Error] {e}")
            raise AudioProcessingError("Something exploded during download.")

    @staticmethod
    def process_nightcore(input_path: str, params: dict) -> str:
        """Processes the audio file into nightcore using ffmpeg."""
        print(f"[AudioService] Processing: {input_path}")
        
        mode = params.get('mode', 'custom')
        format_ext = params.get('format', 'flac')
        
        # Preset Filters (from your bash script)
        presets = {
            'pedo': 'asetrate=44100*1.35,aresample=44100,atempo=1.0',
            'adult': 'asetrate=44100*1.20,aresample=44100,equalizer=f=3000:t=q:w=1:g=3,equalizer=f=8000:t=q:w=1:g=2',
            'best': 'asetrate=44100*1.27,aresample=44100,equalizer=f=3000:t=q:w=1:g=3,equalizer=f=8000:t=q:w=1:g=2',
            'vocalfree': 'pan=stereo|c0=c0-c1|c1=c1-c0,highpass=f=120,lowpass=f=16000'
        }

        if mode in presets:
             audio_filter = presets[mode]
        else:
            # Custom Logic
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
             pass
