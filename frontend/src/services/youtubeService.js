const API_BASE_URL = 'http://localhost:8000';

export const youtubeService = {
  async getVideoId({ title, artist }) {
    try {
      const response = await fetch(
        `${API_BASE_URL}/track/youtube-track?${new URLSearchParams({
          track_title: title,
          artist: artist
        })}`
      );

      if (!response.ok) {
        throw new Error('Failed to fetch video ID');
      }

      const data = await response.json();
      console.log('YouTube API Response:', data); // Debug log

      if (!data.video_id) {
        throw new Error('No video ID returned');
      }

      return data.video_id;
    } catch (error) {
      console.error('Error fetching video ID:', error);
      throw error;
    }
  }
};