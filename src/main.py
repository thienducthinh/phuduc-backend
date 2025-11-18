from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import router
from src.models import init_db
from src.config import settings
# from dotenv import load_dotenv
# import os

# load_dotenv()  # Load .env
# FRONT_END_URL = os.getenv("FRONTEND_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGINS],  # Allow your front-end origin (add more if needed, or ["*"] for all - insecure for prod)
    allow_credentials=True,  # If using cookies/auth
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_db()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)