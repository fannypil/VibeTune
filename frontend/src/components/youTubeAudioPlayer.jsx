import React, { useEffect, useRef, useState } from "react";

export default function YouTubeAudioPlayer({ videoId, isPlaying, volume, onEnd }) {
  const playerRef = useRef(null);
  const playerInstance = useRef(null);
  const [playerReady, setPlayerReady] = useState(false);

    // Load the YouTube IFrame API script ONCE
  useEffect(() => {
    if (!window.YT) {
      const tag = document.createElement('script');
      tag.src = 'https://www.youtube.com/iframe_api';
      document.body.appendChild(tag);
    }
  }, []);

     // Create the player ONCE when the API is ready and videoId is set
  useEffect(() => {
    function createPlayer() {
      if (playerInstance.current) {
        playerInstance.current.loadVideoById(videoId);
        return;
      }
      playerInstance.current = new window.YT.Player('youtube-player', {
        height: "300",
        width: "400",
        videoId,
        playerVars: { autoplay: 0, controls: 1 },
        events: {
          onReady: (event) => {
            event.target.setVolume(volume);
            setPlayerReady(true);
            console.log("YouTube player ready", event.target);
          },
          onStateChange: (event) => {
            if (event.data === window.YT.PlayerState.ENDED) onEnd?.();
          }
        }
      });
    }

    if (window.YT && videoId) {
      createPlayer();
    } else {
      window.onYouTubeIframeAPIReady = () => {
        if (videoId) createPlayer();
      };
    }
    // eslint-disable-next-line
  }, [videoId, volume, onEnd]);

      // Play/Pause logic
    useEffect(() => {
    console.log("Play/Pause effect:", { isPlaying, player: playerInstance.current, playerReady });
    if (playerInstance.current && playerReady) {
      if (isPlaying) {
        playerInstance.current.playVideo();
      } else {
        playerInstance.current.pauseVideo();
      }
    }
  }, [isPlaying, playerReady]);
  // Volume logic
  useEffect(() => {
    if (playerInstance.current && playerReady) {
      playerInstance.current.setVolume(volume);
    }
  }, [volume, playerReady]);

console.log("Loading YouTube videoId:", videoId);
return <div id="youtube-player" style={{ width: 0, height: 0, overflow: "hidden" }} />;
}