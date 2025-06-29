import React, { useState, useEffect } from "react";
import { Loader2, Plus, Music, Play, MoreHorizontal, Users, Lock, Heart } from "lucide-react";
import { playlistService } from "../services/playlistService";
import TrackCard from "../components/trackCard";

export default function Playlists() {
  const [playlists, setPlaylists] = useState([]);
  const [favoritePlaylists, setFavoritePlaylists] = useState([]);
  const [activeTab, setActiveTab] = useState('my-playlists');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadPlaylists();
  }, [activeTab]);

  const loadPlaylists = async () => {
    setIsLoading(true);
    setError(null);
    try {
      if (activeTab === 'my-playlists') {
        const data = await playlistService.getPlaylists();
        setPlaylists(data);
      } else {
        const data = await playlistService.getFavoritePlaylists();
        setFavoritePlaylists(data);
      }
    } catch (error) {
      console.error("Error loading playlists:", error);
      setError("Failed to load playlists");
    } finally {
      setIsLoading(false);
    }
  };

  // Tab navigation component
  const TabNavigation = () => (
    <div className="flex gap-4 mb-8 border-b border-gray-200">
      <button
        onClick={() => setActiveTab('my-playlists')}
        className={`flex items-center gap-2 px-6 py-3 font-medium transition-all border-b-2 -mb-[2px] ${
          activeTab === 'my-playlists'
            ? 'border-purple-500 text-purple-700'
            : 'border-transparent text-gray-500 hover:text-gray-700'
        }`}
      >
        <Music className="w-5 h-5" />
        My Playlists
      </button>
      <button
        onClick={() => setActiveTab('favorites')}
        className={`flex items-center gap-2 px-6 py-3 font-medium transition-all border-b-2 -mb-[2px] ${
          activeTab === 'favorites'
            ? 'border-purple-500 text-purple-700'
            : 'border-transparent text-gray-500 hover:text-gray-700'
        }`}
      >
        <Heart className="w-5 h-5" />
        Favorite Playlists
      </button>
    </div>
  );

  const currentPlaylists = activeTab === 'my-playlists' ? playlists : favoritePlaylists;

  return (
  <div className="p-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between gap-4 mb-6">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center">
              {activeTab === 'favorites' ? (
                <Heart className="w-8 h-8 text-white" />
              ) : (
                <Music className="w-8 h-8 text-white" />
              )}
            </div>
            <div>
              <h1 className="text-4xl font-bold text-gray-900">
                {activeTab === 'favorites' ? 'Favorite Playlists' : 'My Playlists'}
              </h1>
              <p className="text-xl text-gray-600">
                {activeTab === 'favorites' ? 'Your liked playlists' : 'Organize your favorite tracks'}
              </p>
            </div>
          </div>
          {activeTab === 'my-playlists' && (
            <button
              onClick={() => {/* Add create playlist logic */}}
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-medium rounded-xl shadow-lg hover:from-purple-700 hover:to-indigo-700 transition-all flex items-center gap-2"
            >
              <Plus className="w-5 h-5" />
              Create Playlist
            </button>
          )}
        </div>
      </div>

      {/* Tab Navigation */}
      <TabNavigation />

      {/* Error Message */}
      {error && (
        <div className="text-center py-4 px-6 bg-red-50 text-red-600 rounded-xl mb-8">
          {error}
        </div>
      )}

      {/* Playlists Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array(6).fill(0).map((_, i) => (
            <div key={i} className="bg-white rounded-xl p-6 shadow-lg animate-pulse">
              <div className="w-full aspect-square bg-gray-200 rounded-xl mb-4"></div>
              <div className="h-4 bg-gray-200 rounded mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-2/3"></div>
            </div>
          ))}
        </div>
      ) : currentPlaylists.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {currentPlaylists.map((playlist) => (
            <div 
              key={playlist.id} 
              className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all group"
            >
              <div className="aspect-square rounded-lg overflow-hidden mb-4 relative">
                {playlist.cover_image ? (
                  <img 
                    src={playlist.cover_image} 
                    alt={playlist.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                ) : (
                  <div className="w-full h-full bg-gradient-to-br from-purple-100 to-indigo-100 flex items-center justify-center">
                    <Music className="w-12 h-12 text-indigo-600" />
                  </div>
                )}
                
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
                  <button className="w-14 h-14 rounded-full bg-white shadow-lg flex items-center justify-center hover:scale-110 transition-transform">
                    <Play className="w-6 h-6 text-gray-900 ml-1" />
                  </button>
                </div>
              </div>

              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-bold text-gray-900 mb-1">{playlist.name}</h3>
                  <p className="text-sm text-gray-600 mb-2">{playlist.description}</p>
                </div>
                <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                  <MoreHorizontal className="w-5 h-5 text-gray-500" />
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
           <div className="text-center py-16">
          <div className="w-20 h-20 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
            {activeTab === 'favorites' ? (
              <Heart className="w-10 h-10 text-gray-400" />
            ) : (
              <Music className="w-10 h-10 text-gray-400" />
            )}
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            {activeTab === 'favorites' ? 'No favorite playlists yet' : 'No playlists yet'}
          </h3>
          <p className="text-gray-600 mb-6">
            {activeTab === 'favorites' 
              ? 'Start adding playlists to your favorites'
              : 'Start creating your first playlist'
            }
          </p>
          {activeTab === 'my-playlists' && (
            <button 
              onClick={() => {/* Add create playlist logic */}}
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-medium rounded-xl shadow-lg hover:from-purple-700 hover:to-indigo-700 transition-all flex items-center gap-2 mx-auto"
            >
              <Plus className="w-5 h-5" />
              Create Your First Playlist
            </button>
          )}
        </div>
      )}
    </div>
  );
}