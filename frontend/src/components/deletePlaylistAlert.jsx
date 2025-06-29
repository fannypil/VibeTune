import React from "react";
import { XIcon } from "lucide-react";

export default function DeletePlaylistAlert({ isOpen, onClose, onConfirm, playlistTitle }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Delete Playlist</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <XIcon className="w-6 h-6" />
          </button>
        </div>

        <div className="space-y-4">
          <p className="text-gray-600">
            Are you absolutely sure? This action cannot be undone. This will permanently delete the playlist 
            "<span className="font-semibold text-gray-900">{playlistTitle}</span>" 
            and remove all its data.
          </p>

          <div className="flex justify-end gap-3 pt-4">
            <button
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              Cancel
            </button>
            <button
              onClick={onConfirm}
              className="px-4 py-2 text-white bg-red-600 rounded-lg hover:bg-red-700"
            >
              Yes, delete playlist
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}