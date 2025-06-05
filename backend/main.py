from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.playlist import router as playlist_router
from routes.lastfm import router as lastfm_router
from routes.auth import router as auth_router
from routes.playlist import router as playlist_router

app = FastAPI()

# Importing the playlist router
app.include_router(playlist_router)
app.include_router(lastfm_router)
app.include_router(auth_router)
app.include_router(playlist_router)

# Allow CORS for frontend
app.add_middleware(CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"])

@app.get("/", response_model=dict)
async def root():
    return {"message": "Welcome to VibeTune backend!"}

