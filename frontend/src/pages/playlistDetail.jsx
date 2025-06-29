import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Play, Pencil, Trash2, Music,Loader2 } from "lucide-react";
import { playlistService } from "../services/playlistService";
import RenamePlaylistDialog from "../components/renamePlaylistDialog";
import DeletePlaylistAlert from "../components/deletePlaylistAlert";


export default function PlaylistDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [playlist, setPlaylist] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showRenameDialog, setShowRenameDialog] = useState(false);
  const [showDeleteAlert, setShowDeleteAlert] = useState(false);
  const [removingTrackId, setRemovingTrackId] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    loadPlaylistData();
  }, [id]);

  const loadPlaylistData = async () => {
    if (!id) {
      navigate('/playlists');
      return;
    }

    setIsLoading(true);
    try {
      const data = await playlistService.getPlaylistById(id);
      setPlaylist(data);
    } catch (error) {
      console.error("Error loading playlist:", error);
      navigate('/playlists');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 animate-spin text-purple-600" />
      </div>
    );
  }
   const handleRenamePlaylist = async (newName) => {
    try {
      await playlistService.updatePlaylist(id, { 
        name: newName,
        description: playlist.description 
      });
      setShowRenameDialog(false);
      loadPlaylistData(); // Reload playlist data
    } catch (error) {
      console.error("Error renaming playlist:", error);
    }
  };

 const handleDeletePlaylist = async () => {
    try {
      setIsDeleting(true);
      setShowDeleteAlert(false);
      
      // Wait for animation
      await new Promise(resolve => setTimeout(resolve, 300));
      
      await playlistService.deletePlaylist(id);
      navigate('/playlists');
    } catch (error) {
      console.error("Error deleting playlist:", error);
      setIsDeleting(false);
    }
  };

 const handleRemoveTrack = async (trackId) => {
    try {
      setRemovingTrackId(trackId);
      
      // Wait for animation
      await new Promise(resolve => setTimeout(resolve, 300));
      
      await playlistService.removeTrackFromPlaylist(id, trackId);
      await loadPlaylistData();
    } catch (error) {
      console.error("Error removing track:", error);
      alert("Failed to remove track. Please try again.");
    } finally {
      setRemovingTrackId(null);
    }
  };

  return (
    <div className={`p-8 max-w-7xl mx-auto transition-all duration-300 ${
      isDeleting ? 'animate-fade-out-scale' : ''
    }`}>
    <div className="p-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-start gap-8 mb-8">
        <div className="w-48 h-48 bg-gradient-to-br from-purple-100 to-indigo-200 rounded-2xl shadow-lg flex-shrink-0">
          <div className="w-full h-full flex items-center justify-center">
            <Music className="w-16 h-16 text-indigo-600" />
          </div>
        </div>
        
        <div className="flex-grow pt-2">
          <h1 className="text-5xl font-bold text-gray-900 tracking-tight mb-3">
            {playlist?.name}
          </h1>
          <p className="text-gray-600 mb-4">{playlist?.description}</p>
          
          <div className="flex items-center gap-3">
            <button className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-medium rounded-xl shadow-lg hover:from-purple-700 hover:to-indigo-700 transition-all flex items-center gap-2">
              <Play className="w-5 h-5" /> Play All
            </button>
            
            <button 
              onClick={() => setShowRenameDialog(true)}
              className="px-6 py-3 bg-white text-gray-700 font-medium rounded-xl shadow-lg hover:bg-gray-50 transition-all flex items-center gap-2"
            >
              <Pencil className="w-4 h-4" /> Rename
            </button>
            
            <button 
              onClick={() => setShowDeleteAlert(true)}
              className="px-6 py-3 bg-red-50 text-red-600 font-medium rounded-xl shadow-lg hover:bg-red-100 transition-all flex items-center gap-2"
            >
              <Trash2 className="w-4 h-4" /> Delete
            </button>
            
            <button 
              onClick={() => navigate('/playlists')}
              className="px-6 py-3 text-gray-600 font-medium rounded-xl hover:bg-gray-100 transition-all flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" /> Back
            </button>
          </div>
        </div>
      </div>

      {/* Tracks Table */}
      <div className="bg-white shadow-lg rounded-2xl overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-500">#</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-500">Title</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-500">Artist</th>
              <th className="px-6 py-4 text-right text-sm font-medium text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody>
            {playlist?.tracks?.map((track, index) => (
               <tr 
                key={track.id} 
                className={`group hover:bg-gray-50 transition-all duration-300
                ${removingTrackId === track.id ? 'animate-fade-out' : 'opacity-100'}`}
                >
                <td className="px-6 py-4 text-gray-500">{index + 1}</td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-gray-200 rounded-md flex items-center justify-center">
                      <Music className="w-4 h-4 text-gray-400" />
                    </div>
                    <span className="font-medium text-gray-900">{track.name}</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-gray-600">{track.artist}</td>
                <td className="px-6 py-4 text-right">
                  <button 
                    className="p-2 text-gray-400 hover:text-red-600 opacity-0 group-hover:opacity-100 transition-all"
                    onClick={() => handleRemoveTrack(track.id)}
                    disabled={removingTrackId === track.id}
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
        <RenamePlaylistDialog
        isOpen={showRenameDialog}
        onClose={() => setShowRenameDialog(false)}
        currentName={playlist?.name}
        onSave={handleRenamePlaylist}
      />

      <DeletePlaylistAlert
        isOpen={showDeleteAlert}
        onClose={() => setShowDeleteAlert(false)}
        onConfirm={handleDeletePlaylist}
        playlistTitle={playlist?.name}
      />
    </div>
    </div>
  );
}