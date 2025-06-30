import React, { useState, useEffect } from "react";
import { Play, Pause, SkipBack, SkipForward, Volume2, VolumeX } from "lucide-react";
import YouTubeAudioPlayer from "./youTubeAudioPlayer";
import { youtubeService } from "../services/youtubeService";

export default function MusicPlayer({ track, isPlaying, setIsPlaying, volume, setVolume, onNext, onPrevious }) {

  const videoIdForTesting = 'aSugSGCC12I'; // Sabrina Carpenter - Manchild
  const [videoId, setVideoId] = useState(null);

  // Fetch YouTube videoId only when track changes
    useEffect(() => {
    let isMounted = true;
    if (track) {
        youtubeService.getVideoId({ title: track.title || track.name, artist: track.artist })
        .then(id => { if (isMounted) setVideoId(id); })
        .catch(() => setVideoId(null));
    }
    return () => { isMounted = false; };
    }, [track]);

    console.log("MusicPlayer render", { isPlaying, volume, videoId });
  if (!track) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white/95 shadow-2xl border-t z-50">
      <YouTubeAudioPlayer
        videoId={videoId}
        isPlaying={isPlaying}
        volume={volume}
        onEnd={onNext}
      />
      <div className="flex items-center justify-between px-6 h-20">
        <div className="flex items-center gap-4 min-w-0 flex-1">
          <div className="w-12 h-12 bg-gradient-to-br from-gray-200 to-gray-300 rounded-lg overflow-hidden shadow-lg">
            {track.image ? (
              <img src={track.image} alt={track.title || track.name} className="w-full h-full object-cover" />
            ) : (
              <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-indigo-100 to-purple-200">
                <Play className="w-4 h-4 text-indigo-600" />
              </div>
            )}
          </div>
          <div className="min-w-0 flex-1">
            <h4 className="font-semibold text-gray-900 truncate text-sm">{track.title || track.name}</h4>
            <p className="text-gray-600 truncate text-xs">{track.artist}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={onPrevious} className="p-2 rounded-full hover:bg-gray-100">
            <SkipBack className="w-5 h-5" />
          </button>
          <button
            className="w-10 h-10 rounded-full bg-gradient-to-r from-purple-600 to-indigo-600 flex items-center justify-center shadow-lg"
            onClick={() => setIsPlaying(!isPlaying)}
            disabled={!videoId}
          >
            {isPlaying ? <Pause className="w-5 h-5 text-white" /> : <Play className="w-5 h-5 text-white ml-0.5" />}
          </button>
          <button onClick={onNext} className="p-2 rounded-full hover:bg-gray-100">
            <SkipForward className="w-5 h-5" />
          </button>
        </div>
        <div className="flex items-center gap-3 min-w-0 flex-1 justify-end">
          <button className="p-2 rounded-full hover:bg-gray-100" onClick={() => setVolume(volume === 0 ? 70 : 0)}>
            {volume === 0 ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
          </button>
          <input
            type="range"
            min="0"
            max="100"
            value={volume}
            onChange={e => {
                setVolume(Number(e.target.value));
                console.log("Slider changed to", e.target.value);
                }}
            className="w-20 accent-purple-600"
          />
        </div>
      </div>
    </div>
  );
}