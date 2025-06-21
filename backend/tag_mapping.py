

AI_TO_LASTFM_TAGS = {
    "uplifting": ["happy"],
    "motivational": ["power pop", "pop rock"],
    "hopeful": ["indie pop", "dream pop", "happy"],
    "calm": ["ambient", "chillout", "acoustic"],
    "energetic": ["dance", "electropop", "party", "upbeat"],
    "romantic": ["love songs", "r&b", "soft rock"],
    "sad": ["sad", "melancholy"],
    "chill": ["chillout", "lo-fi", "downtempo"],
    "relaxing": ["chillout", "ambient", "acoustic"],
    "happy": ["happy", "feelgood", "pop"],
    "party": ["party", "dance", "club"],
    "melancholy": ["melancholy", "sad"],
    "angry": ["metal", "punk", "hard rock"],
    "nostalgic": ["classic rock", "oldies", "retro"],
    "summer": ["summer", "surf rock", "tropical"],
    "focus": ["instrumental", "study", "ambient"],
    "fun": ["pop", "dance", "party"],
    "epic": ["epic", "soundtrack", "orchestral"],
    "groovy": ["funk", "soul", "groove"],
    "dreamy": ["dream pop", "shoegaze", "ambient"],
}

def map_ai_tags_to_lastfm(ai_tags):
    mapped = []
    for tag in ai_tags:
        tag_lower = tag.lower().strip()
        if tag_lower in AI_TO_LASTFM_TAGS:
            mapped.extend(AI_TO_LASTFM_TAGS[tag_lower])
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for t in mapped:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result