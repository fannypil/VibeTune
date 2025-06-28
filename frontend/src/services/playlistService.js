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
    const response = await fetch(`${API_BASE_URL}/playlists`);
    if (!response.ok) throw new Error('Failed to fetch playlists');
    return response.json();
  },

  async createPlaylist(playlistData) {
    const response = await fetch(`${API_BASE_URL}/playlists`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(playlistData)
    });
    if (!response.ok) throw new Error('Failed to create playlist');
    return response.json();
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
      title: track.title || track.name,
      artist: track.artist,
      image: track.image || "https://placehold.co/400x400?text=No+Image",
      genre: track.genre || "unknown",
      url: track.url || "#",
      duration: track.duration || "0:00"
    }));
  }
};