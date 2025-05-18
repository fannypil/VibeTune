from typing import Dict, List
from models import Track

# Simulate user sessions with in-memory storage
user_playlists: Dict[str, List[Track]] = {}

# Simulate saving and retrieving playlists for users
def save_playlist_for_user(user_id: str, playlist: List[Track]):
    user_playlists[user_id] = playlist

# Function to retrieve a user's playlist
def get_playlist_for_user(user_id: str) -> List[Track]:
    return user_playlists.get(user_id, [])
