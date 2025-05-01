from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from lastfm_services import get_lastfm_top_tracks, search_lastfm_tracks


app = FastAPI()

# Allow CORS for frontend
app.add_middleware(CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "Welcome to VibeTune backend!"}

@app.get("/playlist")
async def get_playlist():
    playlist = [
        {"title": "Song A", "artist": "Artist 1"},
        {"title": "Song B", "artist": "Artist 2"},
        {"title": "Song C", "artist": "Artist 3"},
    ]
    return playlist

@app.get("/lastfm-top-tracks")
async def lastfm_top_tracks():
    try:
        data = get_lastfm_top_tracks()
        return data
    except Exception as e:
        return {"error": str(e)}
    
    
@app.get("/search")
async def search_tracks(q: str = Query(..., description="Song name or artist to search")):
    try:
        results = search_lastfm_tracks(q)
        simplified = [
            {
                "name": track.get("name"),
                "artist": track.get("artist"),
                "url": track.get("url")
            }
            for track in results
        ]
        return {"results": simplified}
    except Exception as e:
        return {"error": str(e)}