import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  Users, 
  Disc, 
  PlayCircle, 
  Loader2 
} from 'lucide-react';
import '../styles/trending.css'; // Assuming you have a CSS file for styles
const tabs = [
  { id: 'tracks', label: 'Hot Tracks', icon: Disc },
  { id: 'artists', label: 'Popular Artists', icon: Users },
];

export default function Trending() {
  const [activeTab, setActiveTab] = useState('tracks');
  const [tracks, setTracks] = useState([]);
  const [artists, setArtists] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, [activeTab]);

  const loadData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      if (activeTab === 'tracks') {
        const response = await fetch('http://localhost:8000/lastfm-top-tracks');
        const data = await response.json();
        setTracks(data.results || []);
      } else {
        const response = await fetch('http://localhost:8000/lastfm-top-artists');
        const data = await response.json();
        setArtists(data || []);
      }
    } catch (err) {
      setError('Failed to load trending content');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center gap-4 mb-8">
        <div className="w-16 h-16 bg-gradient-to-br from-orange-500 to-pink-500 rounded-2xl flex items-center justify-center">
          <TrendingUp className="w-8 h-8 text-white" />
        </div>
        <div>
          <h1 className="text-4xl font-bold text-gray-900">Trending Now</h1>
          <p className="text-xl text-gray-600">Discover what's hot right now</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex space-x-2 mb-8">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`tab-button ${
            activeTab === tab.id ? 'tab-button-active' : 'tab-button-inactive'
           }`}
          >
            <tab.icon className="w-5 h-5 mr-2" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      {isLoading ? (
      <div className="flex items-center justify-center h-64">
      <Loader2 className="loader w-8 h-8" />
        </div>
      ) : activeTab === 'tracks' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tracks.map((track, index) => (
            <div
              key={`${track.name}-${track.artist}`}
              className="relative bg-white rounded-xl p-6 shadow-lg transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
            >
        <div className={`rank-badge ${index < 3 ? `rank-badge-${index + 1}` : 'bg-gray-500 text-white'}`}>
                {index + 1}
              </div>
              <div className="flex items-start gap-4">
                <div className="w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center group-hover:bg-purple-50 transition-colors">
                  <PlayCircle className="w-8 h-8 text-purple-600" />
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-900 group-hover:text-purple-600 transition-colors">
                    {track.name}
                  </h3>
                  <p className="text-gray-600 text-sm">{track.artist}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {artists.map((artist, index) => (
            <div
              key={artist.name}
              className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all hover:-translate-y-1"
            >
              <div className="w-full aspect-square rounded-lg overflow-hidden mb-4 bg-gray-100">
                {artist.image_large ? (
                  <img
                    src={artist.image_large}
                    alt={artist.name}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <Users className="w-12 h-12 text-gray-400" />
                  </div>
                )}
              </div>
              <h3 className="font-bold text-gray-900 mb-2">{artist.name}</h3>
              <p className="text-sm text-gray-600">
                {artist.listeners?.toLocaleString()} listeners
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}