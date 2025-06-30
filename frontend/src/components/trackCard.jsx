import React from "react";
import { Play, Heart, MoreHorizontal, Music } from "lucide-react";
import { youtubeService } from "../services/youtubeService";

const genreColors = {
  pop: "bg-pink-100 text-pink-800",
  rock: "bg-red-100 text-red-800", 
  jazz: "bg-amber-100 text-amber-800",
  classical: "bg-purple-100 text-purple-800",
  electronic: "bg-cyan-100 text-cyan-800",
  "hip-hop": "bg-emerald-100 text-emerald-800",
  indie: "bg-indigo-100 text-indigo-800"
};

export default function TrackCard({ track, onPlay, onAddToFavorites,readonly }) {
  const {
      title,
      artist,
      image,
      genre = "unknown"
    } = track;
  const handlePlay = () => {
    onPlay(track);
  };
  return (
    <div className="group bg-white/80 backdrop-blur-sm hover:bg-white hover:shadow-2xl transition-all duration-500 hover:-translate-y-2 border-0 shadow-lg rounded-2xl overflow-hidden">
      <div className="relative">
        <div className="w-full aspect-video bg-gradient-to-br from-gray-200 to-gray-300 relative overflow-hidden">
          {track?.image ? (
             <img
                src={image}
                alt={`${title} by ${artist}`}
              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-indigo-100 to-purple-200">
              <Music className="w-8 h-8 text-indigo-600" />
            </div>
          )}
             {/* Play button overlay */}
          {!readonly && (
            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all duration-300 flex items-center justify-center">
              <button
                className="w-14 h-14 rounded-full bg-white/90 hover:bg-white hover:scale-110 transition-all duration-300 opacity-0 group-hover:opacity-100 shadow-2xl flex items-center justify-center"
                onClick={handlePlay}
              >
                <Play className="w-6 h-6 text-gray-800 ml-1" />
              </button>
            </div>
          )}
        </div>

        {/* Genre badge */}
        {track?.genre && (
          <span className={`absolute top-3 left-3 px-2 py-1 rounded-full text-xs font-medium ${genreColors[track.genre.toLowerCase()] || "bg-gray-100 text-gray-800"}`}>
            {track.genre}
          </span>
        )}
      </div>

      <div className="p-6">
        <div className="space-y-3">
          <div>
            <h3 className="font-bold text-gray-900 text-lg leading-tight line-clamp-2 group-hover:text-indigo-600 transition-colors duration-300">
              {title}
            </h3>
            <p className="text-gray-600 font-medium mt-1">{track?.artist}</p>
          </div>

          {/* Action buttons */}
          <div className="flex items-center justify-between pt-2">           
            <button 
              className="p-2 rounded-full hover:bg-gray-100 transition-colors duration-300"
            >
              <MoreHorizontal className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}