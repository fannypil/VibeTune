import React, { useState } from "react";
import { 
  Play, 
  Pause, 
  SkipBack, 
  SkipForward, 
  Volume2, 
  VolumeX, 
  Repeat, 
  Shuffle,
  Heart,
  Maximize2
} from "lucide-react";

export default function YouTubePlayer({ currentTrack, isPlaying, onPlayPause, onNext, onPrevious }) {
  const [volume, setVolume] = useState(75);
  const [isMuted, setIsMuted] = useState(false);
  const [progress, setProgress] = useState(0);

  if (!currentTrack) return null;

  return (
    <div className="fixed bottom-0 left-64 right-0 h-20 bg-white/95 backdrop-blur-lg shadow-2xl border-t border-gray-200/50 z-50">
      {/* Progress bar */}
      <div className="absolute top-0 w-full h-1 bg-gray-200">
        <div 
          className="h-full bg-gradient-to-r from-purple-600 to-indigo-600 transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>

      <div className="flex items-center justify-between px-6 h-full">
        {/* Track Info */}
        <div className="flex items-center gap-4 min-w-0 flex-1">
          <div className="w-12 h-12 bg-gradient-to-br from-gray-200 to-gray-300 rounded-lg overflow-hidden shadow-lg">
            {currentTrack.image ? (
              <img 
                src={currentTrack.image} 
                alt={currentTrack.title}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-indigo-100 to-purple-200">
                <Play className="w-4 h-4 text-indigo-600" />
              </div>
            )}
          </div>
          <div className="min-w-0 flex-1">
            <h4 className="font-semibold text-gray-900 truncate text-sm">{currentTrack.title}</h4>
            <p className="text-gray-600 truncate text-xs">{currentTrack.artist}</p>
          </div>
          <button className="p-2 rounded-full hover:bg-red-50 hover:text-red-600 transition-colors">
            <Heart className="w-4 h-4" />
          </button>
        </div>

        {/* Player Controls */}
        <div className="flex items-center gap-3">
          <button className="p-2 rounded-full hover:bg-gray-100 transition-colors">
            <Shuffle className="w-4 h-4" />
          </button>
          <button 
            className="p-2 rounded-full hover:bg-gray-100 transition-colors"
            onClick={onPrevious}
          >
            <SkipBack className="w-5 h-5" />
          </button>
          <button 
            className="w-10 h-10 rounded-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 flex items-center justify-center shadow-lg transition-colors"
            onClick={onPlayPause}
          >
            {isPlaying ? 
              <Pause className="w-5 h-5 text-white" /> : 
              <Play className="w-5 h-5 text-white ml-0.5" />
            }
          </button>
          <button 
            className="p-2 rounded-full hover:bg-gray-100 transition-colors"
            onClick={onNext}
          >
            <SkipForward className="w-5 h-5" />
          </button>
          <button className="p-2 rounded-full hover:bg-gray-100 transition-colors">
            <Repeat className="w-4 h-4" />
          </button>
        </div>

        {/* Volume Control */}
        <div className="flex items-center gap-3 min-w-0 flex-1 justify-end">
          <button 
            className="p-2 rounded-full hover:bg-gray-100 transition-colors"
            onClick={() => setIsMuted(!isMuted)}
          >
            {isMuted || volume === 0 ? 
              <VolumeX className="w-4 h-4" /> : 
              <Volume2 className="w-4 h-4" />
            }
          </button>
          <input
            type="range"
            min="0"
            max="100"
            value={isMuted ? 0 : volume}
            onChange={(e) => setVolume(Number(e.target.value))}
            className="w-20 accent-purple-600"
          />
          <button className="p-2 rounded-full hover:bg-gray-100 transition-colors">
            <Maximize2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}