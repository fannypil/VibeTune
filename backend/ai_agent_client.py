import httpx
from typing import Dict
from lastfm_client import LastFMClient
import logging
from tag_mapping import map_ai_tags_to_lastfm

logger = logging.getLogger(__name__)

class AIAgentClient:
    def __init__(self, base_url: str = "http://ai_agent:8003"):
        self.base_url = base_url

    async def generate(self, prompt: str) -> Dict:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/generate",
                json={"prompt": prompt}
            )
            response.raise_for_status()
            return response.json()
        
class PlaylistGeneratorService:
    def __init__(self, ai_client=None, lastfm_client=None):
        self.ai_client = ai_client or AIAgentClient()
        self.lastfm_client = lastfm_client or LastFMClient()

    async def generate_playlist(self, prompt: str, track_limit: int = 10):
        ai_result = await self.ai_client.generate(prompt)
        ai_tags = ai_result.get("tags", [])
        logger.info(f"AI tags: {ai_tags}")
        # tags = ai_result.get("tags", [])
        
        # Map AI tags to Last.fm-compatible tags
        tags = map_ai_tags_to_lastfm(ai_tags)
        logger.info(f"Mapped Last.fm tags: {tags}")

         # Fallback to popular tags if none returned
        if not tags:
            tags = ["happy", "pop", "dance", "party", "summer"]
            logger.warning(f"No tags from AI, using fallback tags: {tags}")

        raw_tracks = await self.lastfm_client.get_top_tracks_by_tags(tags, limit=track_limit*5)
        logger.info(f"Sample raw tracks: {[{'name': t.get('name'), 'listeners': t.get('listeners'), 'artist': t.get('artist')} for t in raw_tracks[:5]]}")

        # Filter: remove tracks with few listeners or negative words in title
        filtered = []
        negative_words = {"sad", "melancholy", "depress", "cry", "lonely"}
        for track in raw_tracks:
            logger.info(f"Track: {track.get('name')} | Listeners: {track.get('listeners')} | Artist: {track.get('artist')}")
            title = track.get("name", "").lower()
            try:
                listeners = int(track.get("listeners", "0"))
            except (ValueError, TypeError):
                listeners = 0
            filtered.append(track)
            logger.info(f"Filtering track: {title}, listeners: {listeners}, artist: {track.get('artist')}, type(artist): {type(track.get('artist'))}")
        
        logger.info(f"{len(filtered)} tracks after filtering")

         # Fallback: If still empty, try with even more generic tags
        if not filtered:
            fallback_tags = ["pop", "rock", "happy", "summer", "party"]
            logger.warning(f"No tracks after filtering, retrying with fallback tags: {fallback_tags}")
            raw_tracks = await self.lastfm_client.get_top_tracks_by_tags(fallback_tags, limit=track_limit*5)
            logger.info(f"Sample fallback raw tracks: {[{'name': t.get('name'), 'listeners': t.get('listeners'), 'artist': t.get('artist')} for t in raw_tracks[:5]]}")
            for track in raw_tracks:
                title = track.get("name", "").lower()
                try:
                    listeners = int(track.get("listeners", "0"))
                except (ValueError, TypeError):
                    listeners = 0
                filtered.append(track)
            logger.info(f"{len(filtered)} tracks after fallback filtering")


        # Prioritize: tracks matching multiple tags
        track_scores = {}
        for track in filtered:
            artist=track["artist"]["name"] if isinstance(track["artist"], dict) else track["artist"]
            key = (track["name"], artist)
            track_scores.setdefault(key, {"track": track, "score": 0})
            track_scores[key]["score"] += 1

        # Sort by score (matches), then listeners
        sorted_tracks = sorted(
            track_scores.values(),
            key=lambda x: (x["score"], int(x["track"].get("listeners", "0"))),
            reverse=True
        )

        # Limit to requested number
        final_tracks = [x["track"] for x in sorted_tracks[:track_limit]]
        logger.info(f"Returning {len(final_tracks)} tracks in final playlist")

        return {
            "ai_result": ai_result,
            "tracks": final_tracks
        }