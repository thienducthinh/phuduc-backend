from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env
FRONT_END_URL = os.getenv("FRONTEND_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONT_END_URL],  # Allow your front-end origin (add more if needed, or ["*"] for all - insecure for prod)
    allow_credentials=True,  # If using cookies/auth
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)