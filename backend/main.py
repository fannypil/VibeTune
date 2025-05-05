from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from lastfm_services import get_lastfm_top_tracks, search_lastfm_tracks
from models import Track, SearchResponse


app = FastAPI()

# Allow CORS for frontend
app.add_middleware(CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"])

@app.get("/", response_model=dict)
async def root():
    return {"message": "Welcome to VibeTune backend!"}

# dummy endpoint to simulate a playlist
@app.get("/playlist")
async def get_playlist():
    playlist = [
        {"title": "Song A", "artist": "Artist 1"},
        {"title": "Song B", "artist": "Artist 2"},
        {"title": "Song C", "artist": "Artist 3"},
    ]
    return playlist

@app.get("/lastfm-top-tracks", response_model=SearchResponse)
async def lastfm_top_tracks():
    try:
        tracks = get_lastfm_top_tracks()
        simplified_tracks=[
            Track(
                name=track.get("name"),
                artist=track.get("artist", {}).get("name"),
                url=track.get("url")
            )
            for track in tracks
        ]
        return {"results": simplified_tracks}
    except Exception as e:
        return {"error": str(e)}
    
    
@app.get("/search", response_model=SearchResponse)
async def search_tracks(q: str = Query(..., description="Song name or artist to search")):
    try:
        tracks = search_lastfm_tracks(q)
        simplified_tracks = [
           Track(
                name=track.get("name"),
                artist=track.get("artist"),
                url=track.get("url")
            )
            for track in tracks
        ]
        return {"results": simplified_tracks}
    except Exception as e:
        return {"error": str(e)}