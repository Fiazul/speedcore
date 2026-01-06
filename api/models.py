from pydantic import BaseModel, field_validator
import re
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

    @field_validator('url')
    @classmethod
    def validate_youtube_url(cls, v: str) -> str:
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        if not re.match(youtube_regex, v):
            raise ValueError('That is not a YouTube link, you simpleton. Try again.')
        return v

class GenerateResponse(BaseModel):
    success: bool
    filename: Optional[str] = None
    originalFilename: Optional[str] = None
    error: Optional[str] = None
    sarcasm: Optional[str] = None
