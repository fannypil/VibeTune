import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./Layout";
import Auth from "./pages/auth";
import Home from "./pages/home";
import Generate from "./pages/generate";
import Trending from "./pages/trending";
import Playlists from "./pages/playlists";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Router>
      <Routes>
        {/* Root redirect to auth */}
        <Route path="/" element={<Navigate to="/auth" replace />} />
        
        {/* Auth route */}
        <Route path="/auth" element={<Auth />} />

        {/* Protected routes wrapped in Layout */}
        <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
          <Route path="/home" element={<Home />} />
          <Route path="/playlists" element={<Playlists />} />
          <Route path="/generate" element={<Generate />} />
          <Route path="/trending" element={<Trending />} />
        </Route>

        {/* Catch all redirect to auth */}
        <Route path="*" element={<Navigate to="/auth" replace />} />
      </Routes>
    </Router>
  );
}

export default App;