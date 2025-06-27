import { useState } from "react";
import { Sparkles, Search as SearchIcon, TrendingUp } from "lucide-react";
import TrackCard from "../components/trackCard";

// Test data
const dummyTracks = [
  {
    id: 1,
    title: "Bohemian Rhapsody",
    artist: "Queen",
    genre: "rock",
    duration: "5:55",
    image: "https://i.ytimg.com/vi/fJ9rUzIMcZQ/maxresdefault.jpg",
    youtube_id: "fJ9rUzIMcZQ"
  },
  {
    id: 2,
    title: "Blinding Lights",
    artist: "The Weeknd",
    genre: "pop",
    duration: "3:20",
    image: "https://i.ytimg.com/vi/4NRXx6U8ABQ/maxresdefault.jpg",
    youtube_id: "4NRXx6U8ABQ"
  }
];

const genres = ["All", "Pop", "Rock", "Jazz", "Classical", "Electronic", "Hip-Hop"];

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedGenre, setSelectedGenre] = useState("All");
  const [tracks] = useState(dummyTracks); // Using dummy data

  const handlePlayTrack = (track) => {
    console.log("Playing track:", track);
  };

  const handleAddToFavorites = (track) => {
    console.log("Added to favorites:", track);
  };

  // Filter tracks based on search and genre
  const filteredTracks = tracks.filter(track => {
    const matchesGenre = selectedGenre === "All" || 
      track.genre.toLowerCase() === selectedGenre.toLowerCase();
    const matchesSearch = !searchQuery || 
      track.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      track.artist.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesGenre && matchesSearch;
  });

  return (
    <div className="p-8 max-w-7xl mx-auto">
      {/* Welcome Section */}
      <div className="mb-8">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 bg-purple-600 rounded-2xl flex items-center justify-center">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-4xl font-bold text-gray-900">Welcome back</h1>
            <p className="text-xl text-gray-600">Discover your next favorite song</p>
          </div>
        </div>

        {/* Search Bar */}
        <div className="relative max-w-2xl mb-8">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <SearchIcon className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            placeholder="Search for tracks, artists, or albums..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-xl text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
        </div>

        {/* Genre Filter */}
        <div className="flex flex-wrap gap-2 mb-8">
          {genres.map((genre) => (
            <button
              key={genre}
              onClick={() => setSelectedGenre(genre)}
              className={`px-6 py-2 rounded-full text-sm font-medium transition-colors ${
                selectedGenre === genre
                  ? "bg-purple-600 text-white"
                  : "bg-gray-100 text-gray-600 hover:bg-gray-200"
              }`}
            >
              {genre}
            </button>
          ))}
        </div>
      </div>

      {/* Tracks Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {filteredTracks.map((track) => (
          <TrackCard
            key={track.id}
            track={track}
            onPlay={handlePlayTrack}
            onAddToFavorites={handleAddToFavorites}
          />
        ))}
      </div>
    </div>
  );
}