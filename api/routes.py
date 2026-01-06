import os
import random
import asyncio
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from typing import List

from api.models import GenerateRequest, GenerateResponse
from services.audio_service import AudioService, AudioProcessingError
from core.config import TEMP_FOLDER, SARCASM_SUCCESS, SARCASM_ERROR, BASE_DIR

router = APIRouter()

# Single-request concurrency lock
processing_lock = asyncio.Lock()

@router.get("/", response_class=HTMLResponse)
async def index():
    template_path = os.path.join(BASE_DIR, "templates", "index.html")
    with open(template_path, "r") as f:
        return f.read()

@router.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    if not req.url:
        return GenerateResponse(success=False, error="URL required", sarcasm=random.choice(SARCASM_ERROR))
    
    # Check if locked (to inform user about queue)
    is_busy = processing_lock.locked()
    
    async with processing_lock:
        try:
            # Download
            input_path = AudioService.download_audio(req.url)
            
            # Process
            filename = AudioService.process_nightcore(input_path, req.dict())
            
            sarcasm = random.choice(SARCASM_SUCCESS)
            if is_busy:
                sarcasm = "Finally your turn. " + sarcasm

            return GenerateResponse(
                success=True, 
                filename=filename, 
                sarcasm=sarcasm
            )
            
        except AudioProcessingError as e:
            return GenerateResponse(success=False, error=str(e), sarcasm=e.sarcasm)
        except Exception as e:
            print(f"[API Error] {e}")
            return GenerateResponse(
                success=False, 
                error=str(e), 
                sarcasm=random.choice(SARCASM_ERROR)
            )

@router.get("/download/{filename}")
async def download(filename: str):
    file_path = os.path.join(TEMP_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(
            file_path, 
            media_type='application/octet-stream', 
            filename=filename
        )
    raise HTTPException(status_code=404, detail="File not found")
