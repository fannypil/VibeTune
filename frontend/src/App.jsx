import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import Home from "./pages/home";
import Search from "./pages/search";
import Trending from "./pages/trending";
import Playlists from "./pages/playlists";
import Layout from "./Layout";

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Navigate to="/home" replace />} />
          <Route path="home" element={<Home />} />
          <Route path="playlists" element={<Playlists />} />
          <Route path="search" element={<Search />} />
          <Route path="trending" element={<Trending />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App; 