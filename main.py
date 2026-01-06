import uvicorn
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routes import router
from services.cleanup_service import start_cleanup_service
from core.config import APP_TITLE, VERSION

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
