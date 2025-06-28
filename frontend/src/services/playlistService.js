const API_BASE_URL = 'http://localhost:8000/ai';

export const playlistService = {
  async generateFromQuiz(quizData) {
    try {
      const response = await fetch(`${API_BASE_URL}/playlist-from-quiz`, {
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
      return data.map(track => ({
        id: `${track.title}-${track.artist}`.toLowerCase().replace(/[^a-z0-9]+/g, '-'),
        title: track.title || track.name, // Handle both title and name properties
        artist: track.artist,
        image: track.image || "https://placehold.co/400x400?text=No+Image",
        genre: track.genre || "unknown",
        url: track.url || "#",
        duration: track.duration || "0:00"
      }));
    } catch (error) {
      console.error('Service error:', error);
      throw error;
    }
  },

  async generateFromPrompt(prompt) {
    try {
      const response = await fetch(`${API_BASE_URL}/playlist-from-prompt`, {
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
      return data.map(track => ({
        id: `${track.title}-${track.artist}`.toLowerCase().replace(/[^a-z0-9]+/g, '-'),
        title: track.title || track.name, // Handle both title and name properties
        artist: track.artist,
        image: track.image || "https://placehold.co/400x400?text=No+Image",
        genre: track.genre || "unknown",
        url: track.url || "#",
        duration: track.duration || "0:00"
      }));
    } catch (error) {
      console.error('Service error:', error);
      throw error;
    }
  }
};