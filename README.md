# 🎧 VibeTune
VibeTune AI is an intelligent playlist creation platform that generates personalized music playlists based on your mood, context, or preferences. Users can interact via text or quick quizzes. 

## 🚀 Features

- **Conversational Playlist Builder**: Create custom playlists using text prompts.
- **Genre & Mood Explorer**: Discover playlists by mood (happy, chill), genre (jazz, k-pop), or activity (workout, studying). Optionally, use a fun quiz to generate playlists.
- **Save & Revisit Playlists**: Save playlists with custom names.
- **Stream Music**: Play via YouTube embeds (with partial playback for free accounts).
- **Favorites & Playlist Management**: Mark playlists as favorites, rename, or delete them.
- **Modern UI**: Responsive, accessible, and visually appealing interface built with React and Tailwind CSS.
- **Authentication**: secure JWT-based authentication for user registration and login, and session management.

## 🛠️ Tech Stack

- **Frontend:** React (Vite), Tailwind CSS, JavaScript/JSX
- **Backend:** FastAPI (Python), Pydantic, SQLAlchemy
- **AI Agent:** Python (custom logic for mood/intent parsing)
- **APIs:** YouTube Data API, LastFM API, Deezer API
- **Database:** SQLite (default, can be swapped for PostgreSQL or others)
- **Containerization:** Docker, Docker Compose

## 🏗️ Architecture
VibeTune is built as a microservices-based application:

1. **Frontend-UI**  
   - Built with React (Vite) + Tailwind CSS  
   - Handles user interaction, playlist display, and music playback

2. **Backend API**  
   - FastAPI (Python)  
   - Handles authentication, user sessions, playlist CRUD, and request validation

3. **AI/Mood Agent**  
   - Parses user intent from text or quiz.
   - Generates playlist prompts and interacts with music APIs

4. **Music Engine**  
   - Integrates with YouTube, LastFM, and Deezer APIs  
   - Handles track search, genre exploration, and playlist construction

5. **User Database Service**  
   - Stores user preferences, playlist history, and favorites  
   - Enables personalization and future recommendation logic

## Project Structure
```shell
VibeTune/
├── README.md
├── backend/                  #Main FastAPI backend service
│   ├── main.py               #Entry point for the FastAPI backend server
│   ├── requirements.txt      
│   ├── Dockerfile
│   ├── ai_agent_client.py    #Handles communication with the AI/mood agent for playlist generation
│   ├── playlist_manager.py   #Logic for building and managing playlists from AI or API results.
│   ├── lastfm_client.py      #Integrates with the LastFM API for music metadata and recommendations.
│   ├── youtube_client.py     #Integrates with the YouTube API to find playable music videos.
│   ├── deezer_client.py      #Integrates with the Deezer API for album art and track info.
│   ├── routes/               #API endpoints (ai, auth, lastfm, playlist, track, user)
│   ├── schemas/              #Pydantic schemas
│   ├── tests/                #Backend unit and integration tests.
│   ├── utils/                #Utility/helper functions for the backend
│   ├── db/                   #Database models and connection utilities.
│   └── .env.example          #Example environment file to help set up .env
├── ai_agent/
│   ├── main.py               #Entry point for the AI/mood agent service
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/
    ├── src/
    │   ├── components/       #Reusable React UI components (buttons, forms, playlist cards, etc.)
    │   ├── pages/            #Top-level React pages/views (Home, Login, Playlist, etc.)
    │   ├── services/         #API service modules for backend API calls
    │   ├── App.jsx           #Main React app component and router setup
    │   ├── Layout.jsx        #Shared layout component (header, footer, navigation)
    │   └── ...
    ├── public/
    ├── package.json
    ├── tailwind.config.js
    ├── Dockerfile
    └── ...
```

---
## 🖥️ Screenshots & Demo

[![Watch the demo](https://img.youtube.com/vi/3R3Pl6spcmI/hqdefault.jpg)](https://www.youtube.com/watch?v=3R3Pl6spcmI)

**[Demo Video Coming Soon]**

---
## 🔑 Getting API Keys

Before running VibeTune, you’ll need API keys for YouTube and LastFM. Here’s how to get them:

### 1. YouTube API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Navigate to **APIs & Services > Library**.
4. Search for **YouTube Data API v3** and enable it.
5. Go to **APIs & Services > Credentials**.
6. Click **Create Credentials** > **API key**.
7. Copy your API key and add it to your `.env.example` file as `YOUTUBE_API_KEY`.

### 2. LastFM API Key

1. Go to the [LastFM API account page](https://www.last.fm/api/account/create).
2. Log in or create a LastFM account.
3. Fill in the application form and submit (It's enough to fill :Contact email and Application name)
4. Copy your API key and add it to your `.env.example` file as `LASTFM_API_KEY`.
5. Copy your Shared secret and add it to your `.env.example` file as `SECRET_KEY`.

---
## 🛠️ Environment Setup

Before running VibeTune, you need to configure your environment variables. This ensures your backend can securely access required API keys and settings.

### 1. Create Your Environment File

1. **Edit `backend/.env.example` in your editor.**  
   Add your API keys and secrets to the appropriate fields:

   ```env
   LASTFM_API_KEY=your_lastfm_api_key_here
   SECRET_KEY=your_generated_secret_key
   DATABASE_URL=sqlite:///./backend.db
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

   - Make sure to replace the placeholders with your actual API keys and secret.
   - You can use the default `DATABASE_URL` for local development, or point to your own database.

2. **Copy the example file to create your actual environment file:**

   ```bash
   cp backend/.env.example backend/.env
   ```

3. **Save your changes.**

> **Note:** Never commit your `.env` file to version control or share it publicly. It contains sensitive credentials.

---

Once your `.env` file is configured, you’re ready to start the application!  
Continue with the [Getting Started](#-getting-started) section to launch VibeTune.

## ⚡️ Getting Started

### Prerequisites

- Docker (recommended) or Python 3.10+ and Node.js 18+
- YouTube API key
- LastFM API key

### Quick Start (with Docker)

```bash
# Clone the repository
git clone https://github.com/yourusername/vibe-tune.git
cd vibe-tune

# Build and run all services
docker-compose up --build
```
---

### 🌐 Accessing the Application

- **Frontend:** [http://localhost:5173](http://localhost:5173)
- **Backend API:** [http://localhost:8000](http://localhost:8000)
- **AI Agent:** [http://localhost:8003](http://localhost:8003)
- **API Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Testing

- Backend:  
  <!-- ```bash
  cd backend
  pytest
  ``` -->

---
## 📬 Contact

For questions or support, please open an issue or contact [fannypilnik@gmail.com](mailto:fannypilnik@gmail.com).

