import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import Home from "./pages/home";
import Search from "./pages/search";
import Trending from "./pages/trending";
import Playlists from "./pages/playlists";
import Layout from "./Layout";

export default function App() {
  console.log('App component rendering'); // Add debug logging

  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/home" />} />
          <Route path="/home" element={<Home />} />
          <Route path="/playlists" element={<Playlists />} />
          <Route path="/search" element={<Search />} />
          <Route path="/trending" element={<Trending />} />
        </Routes>
      </Layout>
    </Router>
  );
}