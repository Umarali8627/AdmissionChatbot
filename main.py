from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.Chatbot.router import chat_router
import os

app = FastAPI(title="Admission Chatbot API", description="API for Admission Chatbot", version="1.0.0")

default_origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:8501",
    "http://127.0.0.1:8501",
]
env_origins = os.getenv("CORS_ORIGINS")
allow_origins = (
    [origin.strip() for origin in env_origins.split(",") if origin.strip()]
    if env_origins
    else default_origins
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Admission Chatbot API!"}

app.include_router(chat_router)
