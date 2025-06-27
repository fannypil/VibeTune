import { useState, useEffect } from "react";
import { Sparkles, Search as SearchIcon, Loader2 } from "lucide-react";
import TrackCard from "../components/trackCard";
import YouTubePlayer from "../components/youtubeplayer";


const genres = [
  { id: "all", label: "All" },
  { id: "pop", label: "Pop" },
  { id: "rock", label: "Rock" },
  { id: "jazz", label: "Jazz" },
  { id: "classical", label: "Classical" },
  { id: "electronic", label: "Electronic" },
  { id: "hip-hop", label: "Hip-Hop" }
];

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedGenre, setSelectedGenre] = useState("all");
  const [tracks, setTracks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentTrack, setCurrentTrack] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);


  useEffect(() => {
    if (selectedGenre === "all") {
      fetchTopTracks();
    } else {
      fetchTracksByGenre(selectedGenre);
    }
  }, [selectedGenre]);

  const fetchTopTracks = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/lastfm-top-tracks');
      const data = await response.json();
      setTracks(data.results.map(track => ({
        id: `${track.name}-${track.artist}`,
        title: track.name,
        artist: track.artist,
        genre: selectedGenre,
        url: track.url,
        image: track.image || "https://placehold.co/400x400?text=No+Image"
      })));
      setError(null);
    } catch (err) {
      setError('Failed to fetch top tracks');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchTracksByGenre = async (genre) => {
    setIsLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/genre/${genre}`);
      const data = await response.json();
      setTracks(data.map(track => ({
        id: `${track.title}-${track.artist}`,
        title: track.title,
        artist: track.artist,
        genre: genre,
        url: track.url,
        image: track.image || "https://placehold.co/400x400?text=No+Image"
      })));
      setError(null);
    } catch (err) {
      setError('Failed to fetch genre tracks');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenreChange = (genre) => {
    setSelectedGenre(genre);
    setSearchQuery(""); // Reset search when changing genre
  };

  const filteredTracks = tracks.filter(track => {
    return !searchQuery || 
      track.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      track.artist.toLowerCase().includes(searchQuery.toLowerCase());
  });

    const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleNext = () => {
    // Implement next track logic
    console.log("Next track");
  };

  const handlePrevious = () => {
    // Implement previous track logic
    console.log("Previous track");
  };

  return (
    <>
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
                key={genre.id}
                onClick={() => handleGenreChange(genre.id)}
                className={`px-6 py-2 rounded-full text-sm font-medium transition-colors ${
                  selectedGenre === genre.id
                    ? "bg-purple-600 text-white"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                }`}
              >
                {genre.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tracks Grid */}
        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <Loader2 className="w-8 h-8 animate-spin text-purple-600" />
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <p className="text-red-500">{error}</p>
          </div>
        ) : filteredTracks.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500">No tracks found</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {filteredTracks.map((track) => (
              <TrackCard
                key={track.id}
                track={track}
                onPlay={() => {
                  setCurrentTrack(track);
                  setIsPlaying(true);
                }}
                onAddToFavorites={() => console.log("Added to favorites:", track)}
              />
            ))}
          </div>
        )}
      </div>
      <YouTubePlayer
        currentTrack={currentTrack}
        isPlaying={isPlaying}
        onPlayPause={handlePlayPause}
        onNext={handleNext}
        onPrevious={handlePrevious}
      />
    </>
  );
}