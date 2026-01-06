from pydantic import BaseModel
from typing import Optional

class GenerateRequest(BaseModel):
    url: str
    mode: str = "custom"
    format: str = "flac"
    sampleRate: float = 1.2
    tempo: float = 1.0
    bassBoost: int = 0
    midBoost: int = 0
    trebleBoost: int = 0

class GenerateResponse(BaseModel):
    success: bool
    filename: Optional[str] = None
    originalFilename: Optional[str] = None
    error: Optional[str] = None
    sarcasm: Optional[str] = None
