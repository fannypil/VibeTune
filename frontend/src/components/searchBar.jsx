import React, { useState } from "react";
import { Search } from "lucide-react";

export default function SearchBar({ onSearchResults, onSearchChange }) {
    const [searchQuery, setSearchQuery] = useState("")
    const[isSearching, setIsSearching] = useState(false);

const handleSubmit = async (e) => {
    e.preventDefault();
    // Prevent search if the input is empty
    if (!searchQuery.trim()){
        onSearchResults(null)
        return;
    }

    setIsSearching(true);
    try {
      const response = await fetch(`http://localhost:8000/search?q=${encodeURIComponent(searchQuery)}`);
      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

     onSearchResults(data.results.map(track => ({
      id: `${track.title}-${track.artist}`,
      title: track.title,
      artist: track.artist,
      genre: 'all',
      url: track.url,
      image: track.image || "https://placehold.co/400x400?text=No+Image"
    })));
    } catch (err) {
      console.error('Search failed:', err);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="relative max-w-2xl mb-8">
      <form onSubmit={handleSubmit}>
        <div className="relative">
          {/* Search Icon */}
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>

          {/* Search Input */}
          <input
            type="text"
            placeholder="Search for tracks or artists ..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="block w-full pl-10 pr-20 py-3 border border-gray-300 rounded-xl text-gray-900 
                     placeholder-gray-500 bg-white/80 backdrop-blur-sm focus:bg-white
                     focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent
                     shadow-lg focus:shadow-xl transition-all duration-300"
          />

          {/* Right-side buttons */}
          <div className="absolute inset-y-0 right-0 flex items-center pr-2 gap-2">
            <button
              type="submit"
              className="p-2 bg-gradient-to-r from-purple-600 to-indigo-600 
                       hover:from-purple-700 hover:to-indigo-700 rounded-xl 
                       shadow-lg transition-all duration-300"
              aria-label="Search"
              disabled={isSearching}
            >
              <Search className="w-5 h-5 text-white" />
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}