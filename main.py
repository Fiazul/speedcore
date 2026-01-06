import uvicorn
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import random
from api.routes import router
from services.cleanup_service import start_cleanup_service
from core.config import APP_TITLE, VERSION, SARCASM_ERROR

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print(f"Starting {APP_TITLE} v{VERSION}...")
    start_cleanup_service()
    yield
    # Shutdown logic (optional)
    print(f"Shutting down {APP_TITLE}...")

app = FastAPI(title=APP_TITLE, version=VERSION, lifespan=lifespan)

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
