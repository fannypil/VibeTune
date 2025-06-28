const API_BASE_URL = 'http://localhost:8000';

export const trackService = {
  async getTopTracks() {
    try {
      const response = await fetch(`${API_BASE_URL}/lastfm-top-tracks`);
      const data = await response.json();
      return data.results.map(track => ({
        id: `${track.name}-${track.artist}`,
        title: track.name,
        artist: track.artist,
        genre: 'all',
        url: track.url,
        image: track.image || "https://placehold.co/400x400?text=No+Image"
      }));
    } catch (err) {
      throw new Error('Failed to fetch top tracks');
    }
  },

  async getTracksByGenre(genre) {
    try {
      const response = await fetch(`${API_BASE_URL}/genre/${genre}`);
      const data = await response.json();
      return data.map(track => ({
        id: `${track.title}-${track.artist}`,
        title: track.title,
        artist: track.artist,
        genre: genre,
        url: track.url,
        image: track.image || "https://placehold.co/400x400?text=No+Image"
      }));
    } catch (err) {
      throw new Error('Failed to fetch genre tracks');
    }
  },

   async getTrendingTracks() {
    try {
      const response = await fetch(`${API_BASE_URL}/lastfm-top-tracks`);
      const data = await response.json();
      return data.results || [];
    } catch (err) {
      throw new Error('Failed to fetch trending tracks');
    }
  },

  async getTrendingArtists() {
    try {
      const response = await fetch(`${API_BASE_URL}/lastfm-top-artists`);
      const data = await response.json();
      return data || [];
    } catch (err) {
      throw new Error('Failed to fetch trending artists');
    }
  }
};