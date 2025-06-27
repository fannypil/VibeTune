import React from "react";
import { Link, useLocation, Outlet } from "react-router-dom"; 
import { Home, Music, Search, User, TrendingUp, Disc3 } from "lucide-react";


const navigationItems = [
  {
    title: "Home",
    url: "/home",
    icon: Home,
  },
  {
    title: "My Playlists",
    url: "/playlists",
    icon: Music,
  },
  {
    title: "Search Tracks",
    url: "/search",
    icon: Search,
  },
  {
    title: "Trending",
    url: "/trending",
    icon: TrendingUp,
  },
];

export default function Layout() {
  const location = useLocation();

  return (
    <div className="flex h-screen overflow-hidden bg-white">

      {/* Fixed Sidebar */}
      <nav className="w-64 h-screen custom-gradient fixed left-0 top-0 z-40 shadow-2xl">
        {/* Logo Section */}
        <div className="h-20 flex items-center px-6 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 gold-gradient rounded-xl flex items-center justify-center shadow-lg">
              <Disc3 className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white tracking-tight">VibeTune</h1>
              <p className="text-xs text-white/60 font-medium">Premium Music</p>
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <div className="py-8 px-4">
          {navigationItems.map((item) => (
            <Link
              key={item.title}
              to={item.url}
              className={`nav-item-hover flex items-center px-4 py-4 mb-2 rounded-xl text-white/80 hover:text-white group ${
                location.pathname === item.url ? 'bg-white/10 text-white shadow-lg' : ''
              }`}
            >
              <item.icon className="w-5 h-5 mr-4 group-hover:scale-110 transition-transform duration-300" />
              <span className="font-medium tracking-wide">{item.title}</span>
            </Link>
          ))}
        </div>

        {/* User Profile Section */}
        <div className="absolute bottom-6 left-4 right-4">
          <div className="glass-effect rounded-xl p-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full flex items-center justify-center shadow-lg">
                <User className="w-5 h-5 text-white" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-gray-900 text-sm truncate">Music Lover</p>
                <p className="text-xs text-gray-600 truncate">Premium Member</p>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
    <main className="flex-1 ml-64 min-h-screen overflow-y-auto bg-slate-50">
        <Outlet />
      </main>
    </div>
  );
}