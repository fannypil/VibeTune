import React, { useState } from "react";
import { Mail, Lock, User, Save, Loader2 } from "lucide-react";
import { playlistService } from "../services/playlistService";

const GENRES = [
  "mixed", "pop", "rock", "jazz", "classical", "electronic", 
  "hip-hop", "indie", "country", "r&b", "alternative"
];

export default function SavePlaylistModal({ isOpen, onClose, tracks, onPlaylistSaved }) {
const [playlistData, setPlaylistData] = useState({
  name: "AI Generated Playlist", // Changed from title to name
  description: "Discovered through AI recommendations",
  tracks: tracks // Keep only required fields
});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

const handleSave = async () => {
  if (!playlistData.name.trim()) return;
  
  setIsLoading(true);
  setError('');

  try {
       // Check if token exists
    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please log in to save playlists');
      navigate('/auth');
      return;
    }

    const playlistToSave = {
      name: playlistData.name,
      description: playlistData.description,
      tracks: tracks.map(track => ({
        name: track.title, // Use title as track name
        artist: track.artist,
        url: track.url || null
      }))
    };

    const savedPlaylist = await playlistService.createPlaylist(playlistToSave);
    onPlaylistSaved(savedPlaylist);
    onClose();
  } catch (err) {
    console.error('Save error:', err);
    if (err.message.includes('Authentication')) {
      setError('Please log in again to save playlists');
      navigate('/auth');
    } else {
      setError(err.message || 'Failed to save playlist');
    }
  } finally {
    setIsLoading(false);
  }
};

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <Save className="w-6 h-6" />
            Save Playlist
          </h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            ✕
          </button>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Playlist Title
            </label>
            <input
              type="text"
              value={playlistData.name}
              onChange={(e) => setPlaylistData({ ...playlistData, name: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500"
              placeholder="Enter playlist title"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={playlistData.description}
              onChange={(e) => setPlaylistData({ ...playlistData, description: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 h-24"
              placeholder="Describe your playlist"
            />
          </div>

          <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
            This playlist will contain {tracks.length} AI-recommended tracks.
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <button
              onClick={onClose}
              disabled={isLoading}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={isLoading || !playlistData.name.trim()}
              className="px-4 py-2 text-white bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg hover:from-purple-600 hover:to-pink-600 flex items-center gap-2"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4" />
                  Save Playlist
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}