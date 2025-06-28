import React, { useState,useCallback } from "react";
import { Loader2, Wand2, Sparkles, Music } from "lucide-react";
import { playlistService } from "../services/playlistService";
import TrackCard from "../components/trackCard";

// Mood options with emojis
const moods = [
  { value: "happy", label: "Happy", emoji: "😊" },
  { value: "relaxed", label: "Relaxed", emoji: "😌" },
  { value: "focused", label: "Focused", emoji: "🧐" },
  { value: "sleepy", label: "Sleepy", emoji: "😴" },
  { value: "energetic", label: "Energetic", emoji: "💪" }
];

const activities = [
  { value: "studying", label: "Studying", icon: "📚" },
  { value: "working_out", label: "Working out", icon: "🏃‍♂️" },
  { value: "commuting", label: "Commuting", icon: "🚗" },
  { value: "relaxing", label: "Relaxing", icon: "🛋️" },
  { value: "party", label: "Party", icon: "🎉" }
];

const genres = [
  "Pop", "Rock", "Hip Hop", "R&B", "Electronic", 
  "Jazz", "Classical", "Country"
];
const decades = [
  { value: "80s", label: "80s", icon: "🎸" },
  { value: "90s", label: "90s", icon: "💿" },
  { value: "00s", label: "2000s", icon: "📱" },
  { value: "10s", label: "2010s", icon: "🎧" },
  { value: "20s", label: "2020s", icon: "🎵" }
];

const discoveryModes = [
  { value: "popular", label: "Popular Hits", icon: "🌟" },
  { value: "fresh", label: "Fresh Finds", icon: "🆕" },
  { value: "mix", label: "Balanced Mix", icon: "⚖️" }
];

export default function Generate() {
  const [isLoading, setIsLoading] = useState(false);
  const [tracks, setTracks] = useState([]);
  const [error, setError] = useState(null);
  const [aiPrompt, setAiPrompt] = useState("");
  const [activeTab, setActiveTab] = useState('quiz'); // 'quiz' or 'prompt'

  
  // Quiz state
  const [selectedMood, setSelectedMood] = useState("");
  const [selectedActivity, setSelectedActivity] = useState("");
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [selectedDecade, setSelectedDecade] = useState("");
  const [discoveryMode, setDiscoveryMode] = useState("mix");


  const handleGenreToggle = (genre) => {
    setSelectedGenres(prev => 
      prev.includes(genre) 
        ? prev.filter(g => g !== genre)
        : [...prev, genre]
    );
  };

   const handlePromptSubmit = async (e) => {
  e.preventDefault();
  if (!aiPrompt.trim()) return;
  
  setIsLoading(true);
  try {
    const data = await playlistService.generateFromPrompt(aiPrompt);
    
    console.log('Transformed data:', data); // Debug log
    
    if (!Array.isArray(data) || data.length === 0) {
      throw new Error('No tracks returned');
    }
    
    setTracks(data);
    setError(null);
  } catch (err) {
    console.error('Prompt generation error:', err);
    setError("Failed to generate playlist. Please try again.");
  } finally {
    setIsLoading(false);
  }
};

const handleQuizSubmit = async () => {
  if (!selectedMood || !selectedActivity || selectedGenres.length === 0 || !selectedDecade || !discoveryMode) {
    setError("Please complete all quiz sections");
    return;
  }

  setIsLoading(true);
  try {
    const data = await playlistService.generateFromQuiz({
      mood: selectedMood,
      activity: selectedActivity,
      preferred_genres: selectedGenres,
      decade: selectedDecade,
      discovery_mode: discoveryMode
    });
    
    console.log('Transformed data:', data); // Debug log
    
    if (!Array.isArray(data) || data.length === 0) {
      throw new Error('No tracks returned');
    }
    
    setTracks(data);
    setError(null);
  } catch (err) {
    console.error('Quiz generation error:', err);
    setError("Failed to generate playlist. Please try again.");
  } finally {
    setIsLoading(false);
  }
};
  // Add reset function
  const resetResults = useCallback(() => {
    setTracks([]);
    setError(null);
    setIsLoading(false);
  }, []);

  // Update tab change handler to include reset
  const handleTabChange = (tab) => {
    setActiveTab(tab);
    resetResults();
    if (tab === 'quiz') {
      setAiPrompt('');
    } else {
      setSelectedMood('');
      setSelectedActivity('');
      setSelectedGenres([]);
      setSelectedDecade('');
      setDiscoveryMode('mix');
    }
  };


  return (
    <div className="p-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-4xl font-bold text-gray-900">AI Playlist Generator</h1>
            <p className="text-xl text-gray-600">Create your perfect playlist with AI</p>
          </div>
        </div>
      </div>

     {/* Tab Navigation */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => handleTabChange('quiz')}
          className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all ${
            activeTab === 'quiz'
              ? 'bg-purple-100 text-purple-700 ring-2 ring-purple-400'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          <Music className="w-5 h-5" />
          Quick Mood Quiz
        </button>
        <button
          onClick={() => handleTabChange('prompt')}
          className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all ${
            activeTab === 'prompt'
              ? 'bg-indigo-100 text-indigo-700 ring-2 ring-indigo-400'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          <Wand2 className="w-5 h-5" />
          AI Prompt
        </button>
      </div>

      {/* Content Panel */}
      <div className="bg-white rounded-xl p-6 shadow-lg mb-8">
        {activeTab === 'quiz' ? (
          <div className="space-y-6">
            {/* Mood Selection */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">How are you feeling right now?</h3>
              <div className="grid grid-cols-3 md:grid-cols-5 gap-3">
                {moods.map(mood => (
                  <button
                    key={mood.value}
                    onClick={() => setSelectedMood(mood.value)}
                    className={`flex flex-col items-center p-4 rounded-xl transition-all ${
                      selectedMood === mood.value
                        ? "bg-purple-100 ring-2 ring-purple-400 scale-105"
                        : "bg-gray-50 hover:bg-gray-100"
                    }`}
                  >
                    <span className="text-2xl mb-2">{mood.emoji}</span>
                    <span className="text-sm font-medium text-gray-700">{mood.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Activity Selection */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">What are you doing?</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {activities.map(activity => (
                  <button
                    key={activity.value}
                    onClick={() => setSelectedActivity(activity.value)}
                    className={`flex items-center gap-3 p-4 rounded-xl transition-all ${
                      selectedActivity === activity.value
                        ? "bg-purple-100 ring-2 ring-purple-400"
                        : "bg-gray-50 hover:bg-gray-100"
                    }`}
                  >
                    <span className="text-2xl">{activity.icon}</span>
                    <span className="text-sm font-medium text-gray-700">{activity.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Genre Selection */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Select your preferred genres:</h3>
              <div className="flex flex-wrap gap-2">
                {genres.map(genre => (
                  <button
                    key={genre}
                    onClick={() => handleGenreToggle(genre.toLowerCase())}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                      selectedGenres.includes(genre.toLowerCase())
                        ? "bg-purple-100 text-purple-700 ring-2 ring-purple-400"
                        : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                    }`}
                  >
                    {genre}
                  </button>
                ))}
              </div>
            </div>
            {/* Decade Selection */}
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Which era do you prefer?</h3>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                  {decades.map(decade => (
                    <button
                      key={decade.value}
                      onClick={() => setSelectedDecade(decade.value)}
                      className={`flex flex-col items-center p-4 rounded-xl transition-all ${
                        selectedDecade === decade.value
                          ? "bg-purple-100 ring-2 ring-purple-400 scale-105"
                          : "bg-gray-50 hover:bg-gray-100"
                      }`}
                    >
                      <span className="text-2xl mb-2">{decade.icon}</span>
                      <span className="text-sm font-medium text-gray-700">{decade.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Discovery Mode */}
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Discovery Preference</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {discoveryModes.map(mode => (
                    <button
                      key={mode.value}
                      onClick={() => setDiscoveryMode(mode.value)}
                      className={`flex items-center justify-center gap-3 p-4 rounded-xl transition-all ${
                        discoveryMode === mode.value
                          ? "bg-purple-100 ring-2 ring-purple-400"
                          : "bg-gray-50 hover:bg-gray-100"
                      }`}
                    >
                      <span className="text-2xl">{mode.icon}</span>
                      <span className="text-sm font-medium text-gray-700">{mode.label}</span>
                    </button>
                  ))}
                </div>
              </div>
            <button
              onClick={handleQuizSubmit}
              disabled={isLoading}
              className="w-full py-3 px-4 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-medium rounded-xl shadow-lg hover:from-purple-700 hover:to-indigo-700 transition-all disabled:opacity-50"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 mx-auto animate-spin" />
              ) : (
                "Generate My Playlist"
              )}
            </button>
          </div>
        ) : (
          <form onSubmit={handlePromptSubmit} className="space-y-4">
            <textarea
              value={aiPrompt}
              onChange={(e) => setAiPrompt(e.target.value)}
              placeholder="Describe your perfect playlist... (e.g., 'Create a playlist with upbeat indie rock songs perfect for a road trip through California')"
              className="w-full h-40 p-4 text-gray-700 bg-gray-50 rounded-xl border-0 focus:ring-2 focus:ring-purple-400"
            />
            <button
              type="submit"
              disabled={isLoading || !aiPrompt.trim()}
              className="w-full py-3 px-4 bg-gradient-to-r from-indigo-600 to-blue-600 text-white font-medium rounded-xl shadow-lg hover:from-indigo-700 hover:to-blue-700 transition-all disabled:opacity-50"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 mx-auto animate-spin" />
              ) : (
                "Generate Custom Playlist"
              )}
            </button>
          </form>
        )}
      </div>

      {/* Results Section */}
      {error && (
        <div className="text-center py-4 px-6 bg-red-50 text-red-600 rounded-xl mb-8">
          {error}
        </div>
      )}

      {tracks?.length > 0 && (
        <>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Your Generated Playlist ({tracks.length} tracks)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {tracks.map((track) => (
              <TrackCard
                key={track.id}
                track={track}
                onPlay={() => {
                  console.log("Playing:", track);
                  // Add your play logic here
                }}
                onAddToFavorites={() => {
                  console.log("Added to favorites:", track);
                  // Add your favorites logic here
                }}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}