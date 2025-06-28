import React from "react";

const genres = [
  { id: "all", label: "All", color: "from-gray-100 to-gray-200 text-gray-800" },
  { id: "pop", label: "Pop", color: "from-pink-100 to-rose-200 text-pink-800" },
  { id: "rock", label: "Rock", color: "from-red-100 to-orange-200 text-red-800" },
  { id: "jazz", label: "Jazz", color: "from-amber-100 to-yellow-200 text-amber-800" },
  { id: "classical", label: "Classical", color: "from-purple-100 to-violet-200 text-purple-800" },
  { id: "electronic", label: "Electronic", color: "from-cyan-100 to-blue-200 text-cyan-800" },
  { id: "hip-hop", label: "Hip-Hop", color: "from-emerald-100 to-green-200 text-emerald-800" }
];

export default function GenreFilter({ selectedGenre, onGenreChange }) {
  return (
    <div className="mb-8">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 tracking-wide">
        Browse by Genre
      </h3>
      <div className="flex flex-wrap gap-2">
        {genres.map((genre) => (
          <button
            key={genre.id}
            onClick={() => onGenreChange(genre.id)}
            className={`px-6 py-2 rounded-full text-sm font-medium transition-all duration-300 
                       hover:scale-105 hover:shadow-lg whitespace-nowrap
                       bg-gradient-to-r ${genre.color}
                       ${selectedGenre === genre.id 
                         ? "ring-2 ring-purple-400 shadow-lg transform scale-105" 
                         : "hover:ring-2 hover:ring-purple-200"}`}
          >
            {genre.label}
          </button>
        ))}
      </div>
    </div>
  );
}

// Export genres for reuse
export { genres };