const API_BASE_URL = 'http://localhost:8000';
const AI_BASE_URL = `${API_BASE_URL}/ai`;

export const playlistService = {
  async generateFromQuiz(quizData) {
    try {
      const response = await fetch(`${AI_BASE_URL}/playlist-from-quiz`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mood: quizData.mood,
          activity: quizData.activity,
          preferred_genres: quizData.preferred_genres,
          decade: quizData.decade,
          discovery_mode: quizData.discovery_mode
        })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      console.log('Raw API response:', data); // Debug log
      
      // Transform the data to match TrackCard expectations
      return this.transformTracks(data);
    } catch (error) {
      console.error('Service error:', error);
      throw error;
    }
  },

  async generateFromPrompt(prompt) {
    try {
      const response = await fetch(`${AI_BASE_URL}/playlist-from-prompt`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      console.log('Raw API response:', data); // Debug log

      // Transform the data to match TrackCard expectations
      return this.transformTracks(data);
    } catch (error) {
      console.error('Service error:', error);
      throw error;
    }
  },
  // Playlist Management
async getPlaylists() {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('Authentication required');
  }

  try {
    const response = await fetch(`${API_BASE_URL}/playlist/my-playlists`, {
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to fetch playlists');
    }

    const data = await response.json();
    return data.map(playlist => ({
      id: playlist.id,
      name: playlist.name,
      description: playlist.description,
      created_at: playlist.created_at,
      is_favorite: playlist.is_favorite || false
    }));
  } catch (error) {
    console.error('Error fetching playlists:', error);
    throw error;
  }
},

 async createPlaylist(playlistData) {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    // Debug log
    console.log('Token:', token);

 // Format data according to PlaylistCreate schema
  const requestBody = {
    name: playlistData.name,
    description: playlistData.description,
    tracks: playlistData.tracks.map(track => ({
      name: track.title || track.name, // Track name is required
      artist: track.artist, // Artist is required
      url: track.url || null // URL is optional
    }))
  };

  // Debug log
    console.log('Creating playlist with data:', requestBody);
try{
    const response = await fetch(`${API_BASE_URL}/playlist`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(requestBody)
  });

  // Debug log
  console.log('Response status:', response.status);

  if (!response.ok) {
    const error = await response.json();
    console.error('Server error:', error); // Debug log
    throw new Error(error.detail || 'Failed to create playlist');
  }

   const data = await response.json();
      return data;
    } catch (error) {
      console.error('Playlist creation error:', error);
      throw error;
    }
  },

  async addTracksToPlaylist(playlistId, tracks) {
    const response = await fetch(`${API_BASE_URL}/playlists/${playlistId}/tracks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tracks })
    });
    if (!response.ok) throw new Error('Failed to add tracks to playlist');
    return response.json();
  },

  // Helper methods
transformTracks(tracks) {
  if (!Array.isArray(tracks)) return [];
  
  return tracks.map(track => ({
    id: `${track.title}-${track.artist}`.toLowerCase().replace(/[^a-z0-9]+/g, '-'),
    name: track.name || track.title, 
    title: track.title || track.name,
    artist: track.artist,
    url: track.url || "#",
    image: track.image || "https://placehold.co/400x400?text=No+Image",
    genre: track.genre || "unknown",
    duration: track.duration || "0:00"
  }));
}
};
