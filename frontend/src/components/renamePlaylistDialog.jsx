import React, { useState, useEffect } from "react";
import { XIcon } from "lucide-react";

export default function RenamePlaylistDialog({ isOpen, onClose, currentName, onSave }) {
  const [newName, setNewName] = useState(currentName);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    setNewName(currentName);
  }, [currentName]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newName.trim()) return;
    
    setIsSaving(true);
    try {
      await onSave(newName);
      onClose();
    } catch (error) {
      console.error('Error saving:', error);
    } finally {
      setIsSaving(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Rename Playlist</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <XIcon className="w-6 h-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              New Name
            </label>
            <input
              type="text"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500"
              placeholder="Enter new name"
            />
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSaving || !newName.trim() || newName === currentName}
              className="px-4 py-2 text-white bg-purple-600 rounded-lg hover:bg-purple-700 disabled:opacity-50"
            >
              {isSaving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}