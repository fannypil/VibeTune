from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.playlist import router as playlist_router
from routes.lastfm import router as lastfm_router
from routes.auth import router as auth_router
from routes.playlist import router as playlist_router
from routes.user import router as user_router
from db.session import engine
from db.models import Base


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"])

# Importing the playlist router
app.include_router(playlist_router)
app.include_router(lastfm_router)
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/", response_model=dict)
async def root():
    return {"message": "Welcome to VibeTune backend!"}

