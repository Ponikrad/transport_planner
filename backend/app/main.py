from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME,
              description="Driver routes planning system",
              version="1.0.0", 
              debug=settings.DEBUG
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME}!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
