# 🎧 VibeTune
VibeTune AI is an intelligent playlist creation platform that generates personalized music playlists based on your mood, context, or preferences. Users can interact via text, voice, or quick quizzes. 

## Features

- **Conversational Playlist Builder**: Create custom playlists using text or voice prompts.
- **Genre & Mood Explorer**: Discover playlists by mood (happy, chill), genre (jazz, k-pop), or activity (workout, studying). Optionally, use a fun quiz to generate playlists.
- **Personalized Suggestions**: Tailored recommendations using listening history or a quick preferences quiz.
- **Save & Revisit Playlists**: Save playlists with custom names (stored locally or in a database).
- **Stream Music**: Play via Spotify Web Playback SDK or YouTube embeds, with partial playback for free accounts.

## Microservices Architecture
1. ``Frontend-UI`` - sends mood/activity/text/quiz/voice to backend-core. Displays music & lets user play/save/share playlists.
2. ``Backend`` - Auth, user sessions, routing, request validation (FastAPI + Pydantic).
3. ``Mood-agent`` - Parses user intent from multiple sources (voice, quiz, text), generates playlist prompt.
Includes Voice2Text module internally.
4. ``music-engine`` - Queries Spotify/Youtube APIs for tracks, handles genre exploration & playlist construction.
5. ``user-db-service`` - Stores user preferences, playlist history, shared playlists. Enables personalization & future recommendation logic.

## Project Structure
```shell
VibeTune
    ├── README.md
    ├── backend
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── main.py
    └── frontend
        └── Dockerfile
```

