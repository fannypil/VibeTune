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

    try {
      // First create playlist without tracks
      const response = await fetch(`${API_BASE_URL}/playlist`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          name: playlistData.name,
          description: playlistData.description
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create playlist');
      }

      const playlist = await response.json();
      
      // Then add tracks using the existing endpoint
      if (playlistData.tracks && playlistData.tracks.length > 0) {
        await this.addTracksToPlaylist(playlist.id, playlistData.tracks);
      }

      return playlist;
    } catch (error) {
      console.error('Playlist creation error:', error);
      throw error;
    }
  },

async addTracksToPlaylist(playlistId, tracks) {
  const token = localStorage.getItem('token');
  
  try {
    // Add tracks one by one using the track endpoint
    const addTrackPromises = tracks.map(track => 
      fetch(`${API_BASE_URL}/track/${playlistId}/tracks`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          name: track.name || track.title,
          artist: track.artist,
          url: track.url || null,
          playlist_id: playlistId 
        })
      }).then(response => {
        if (!response.ok) {
          throw new Error('Failed to add track');
        }
        return response.json();
      })
    );

    // Wait for all tracks to be added
    const results = await Promise.all(addTrackPromises);
    console.log('Added tracks:', results);
    
    return results;
  } catch (error) {
    console.error('Error adding tracks:', error);
    throw new Error('Failed to add tracks to playlist');
  }
},
async getFavoritePlaylists() {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('Authentication required');
  }

  try {
    const response = await fetch(`${API_BASE_URL}/playlist/favorites`, {
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      if (response.status === 404) {
        return []; // Return empty array for no favorites
      }
      const error = await response.json();
      throw new Error(error.detail || 'Failed to fetch favorite playlists');
    }

    const data = await response.json();
    return data.map(playlist => ({
      id: playlist.id,
      name: playlist.name,
      description: playlist.description,
      created_at: playlist.created_at,
      is_favorite: true // These are favorite playlists, so always true
    }));
  } catch (error) {
    console.error('Error fetching favorite playlists:', error);
    if (error.message === 'No playlists found') {
      return []; // Return empty array for no playlists found
    }
    throw error;
  }
},
async getPlaylistById(id) {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/playlist/${id}`, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Playlist not found');
        }
        const error = await response.json();
        throw new Error(error.detail || 'Failed to fetch playlist');
      }

      return response.json();
    } catch (error) {
      console.error('Error fetching playlist:', error);
      throw error;
    }
  },
   async updatePlaylist(id, updateData) {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/playlist/${id}`, {
        method: 'PUT',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updateData)
      });

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Playlist not found');
        }
        if (response.status === 403) {
          throw new Error('Not authorized to update this playlist');
        }
        const error = await response.json();
        throw new Error(error.detail || 'Failed to update playlist');
      }

      return response.json();
    } catch (error) {
      console.error('Error updating playlist:', error);
      throw error;
    }
  },
    async deletePlaylist(id) {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/playlist/${id}`, {
        method: 'DELETE',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Playlist not found');
        }
        if (response.status === 403) {
          throw new Error('Not authorized to delete this playlist');
        }
        const error = await response.json();
        throw new Error(error.detail || 'Failed to delete playlist');
      }

      return true; // Success
    } catch (error) {
      console.error('Error deleting playlist:', error);
      throw error;
    }
  },async removeTrackFromPlaylist(playlistId, trackId) {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('Authentication required');
  }

  try {
    const response = await fetch(`${API_BASE_URL}/track/${playlistId}/tracks/${trackId}`, {
      method: 'DELETE',
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Track not found in playlist');
      }
      const error = await response.json();
      throw new Error(error.detail || 'Failed to remove track');
    }

    return true;
  } catch (error) {
    console.error('Error removing track:', error);
    throw error;
  }
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
