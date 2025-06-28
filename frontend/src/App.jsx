import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import Home from "./pages/home";
import Generate from "./pages/generate";
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
          <Route path="generate" element={<Generate />} />
          <Route path="trending" element={<Trending />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App; 