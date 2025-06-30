import { useState, useEffect } from "react";
import { Sparkles, Loader2 } from "lucide-react";
import TrackCard from "../components/trackCard";
import SearchBar from "../components/searchBar";
import GenreFilter from "../components/genreFilter";
import trackService from "../services/musicService";
import MusicPlayer from "../components/musicPlayer";


export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedGenre, setSelectedGenre] = useState("all");
  const [tracks, setTracks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentTrack, setCurrentTrack] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(70);


  useEffect(() => {
    fetchTracks();
  }, [selectedGenre]);

  const fetchTracks = async () => {
    setIsLoading(true);
    try {
      const tracks = selectedGenre === "all" 
        ? await trackService.getTopTracks()
        : await trackService.getTracksByGenre(selectedGenre);
      setTracks(tracks);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

 const handleGenreChange = (genre) => {
  setSelectedGenre(genre);
  setSearchQuery("");
  setCurrentTrack(null); // Stop playback
  setIsPlaying(false);   // Pause player
};

  const handleSearchResults = (searchResults) => {
    if (searchResults === null) {
      // Reset to default tracks when search is cleared
      if (selectedGenre === "all") {
        fetchTopTracks();
      } else {
        fetchTracksByGenre(selectedGenre);
      }
    } else {
      setTracks(searchResults.map(track => ({
        ...track,
        name: track.title || track.name,
      })));
      setSelectedGenre('all');
    }
     setCurrentTrack(null); // Stop playback
     setIsPlaying(false);   // Pause player
  };

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
              <SearchBar onSearchResults={handleSearchResults} />
          </div>

        {/* Genre Filter */}
          <div className="flex flex-wrap gap-2 mb-8">
           <GenreFilter
              selectedGenre={selectedGenre}
              onGenreChange={handleGenreChange}
            />
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
        ) : tracks.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500">No tracks found</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {tracks.map((track) => (
              <TrackCard
                key={track.id || `${track.title || track.name}-${track.artist}-${idx}`}
                track={track}
                readonly={false}
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
      <MusicPlayer
        track={currentTrack}
        isPlaying={isPlaying}
        setIsPlaying={setIsPlaying}
        volume={volume}
        setVolume={setVolume}
        onNext={handleNext}
        onPrevious={handlePrevious}
      />
    </>
  );
}