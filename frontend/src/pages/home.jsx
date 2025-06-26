import { useState } from "react";
import { SparklesIcon, MagnifyingGlassIcon } from "@heroicons/react/24/outline";

const genres = ["All", "Pop", "Rock", "Jazz", "Classical", "Electronic", "Hip-Hop"];

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedGenre, setSelectedGenre] = useState("All");

  return (
    <div className="p-8 max-w-7xl mx-auto">
      {/* Welcome Section */}
      <div className="flex items-center gap-4 mb-8">
        <div className="w-16 h-16 bg-purple-600 rounded-2xl flex items-center justify-center">
          <SparklesIcon width={24} height={24} className="h-8 w-8 text-white" />
        </div>
        <div>
          <h1 className="text-4xl font-bold text-gray-900">Welcome back</h1>
          <p className="text-xl text-gray-600">Discover your next favorite song</p>
        </div>
      </div>

      {/* Search Bar */}
      <div className="relative max-w-2xl mb-8">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <MagnifyingGlassIcon width={24} height={24} className="h-5 w-5 text-gray-400" />
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

      {/* Featured Playlists */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Featured Playlists</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Add your playlist cards here */}
        </div>
      </section>
    </div>
  );
}