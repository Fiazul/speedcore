import uvicorn
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import random
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from api.routes import router
from services.cleanup_service import start_cleanup_service
from core.config import APP_TITLE, VERSION, SARCASM_ERROR

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print(f"Starting {APP_TITLE} v{VERSION}...")
    start_cleanup_service()
    yield
    # Shutdown logic (optional)
    print(f"Shutting down {APP_TITLE}...")

app = FastAPI(title=APP_TITLE, version=VERSION, lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include API routes
app.include_router(router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract the error message from Pydantic
    error_msg = exc.errors()[0].get('msg', 'Invalid input')
    # Remove 'Value error, ' prefix if present
    if error_msg.startswith("Value error, "):
        error_msg = error_msg.replace("Value error, ", "")
    
    return JSONResponse(
        status_code=200, # Still return 200 so the frontend handles it as a normal "fail"
        content={
            "success": False,
            "error": error_msg,
            "sarcasm": random.choice(SARCASM_ERROR)
        }
    )

@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=200, # Keep it 200 for frontend to handle as normal fail
        content={
            "success": False,
            "error": "Slow down! 2 requests per minute. I'm not a robot (actually I am, but a busy one).",
            "sarcasm": "Stop spamming me. My CPU is sensitive."
        }
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
