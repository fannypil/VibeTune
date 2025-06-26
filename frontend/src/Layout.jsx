import React from "react";
import { Link, useLocation } from "react-router-dom";
import { 
  HomeIcon, 
  MusicalNoteIcon, 
  MagnifyingGlassIcon, 
  UserCircleIcon, 
  FireIcon, 
  PlayCircleIcon 
} from "@heroicons/react/24/outline";


const navigationItems = [
  {
    title: "Home",
    url: "/home",
    icon: HomeIcon,
  },
  {
    title: "My Playlists",
    url: "/playlists",
    icon: MusicalNoteIcon,
  },
  {
    title: "Search Tracks",
    url: "/search",
    icon: MagnifyingGlassIcon,
  },
  {
    title: "Trending",
    url: "/trending",
    icon: FireIcon,
  },
];

export default function Layout({ children }) {
  const location = useLocation();

  return (
    <div className="w-full min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <style>
        {`
          :root {
            --primary-navy: #1a1b3a;
            --primary-gold: #f59e0b;
            --accent-purple: #6366f1;
            --soft-gray: #f8fafc;
          }

          .custom-gradient {
            background: linear-gradient(135deg, var(--primary-navy) 0%, #2d3748 100%);
          }

          .gold-gradient {
            background: linear-gradient(135deg, var(--primary-gold) 0%, #f97316 100%);
          }

          .glass-effect {
            backdrop-filter: blur(20px);
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.2);
          }

          .nav-item-hover {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          }

          .nav-item-hover:hover {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%);
            transform: translateX(4px);
          }
        `}
      </style>

      {/* Sidebar */}
      <nav className="w-64 bg-[#1a1b3a] fixed h-full flex flex-col">
        {/* Logo Section */}
        <div className="p-6 border-b border-gray-800">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-orange-500 rounded-2xl flex items-center justify-center">
              <PlayCircleIcon  width={24} height={24} className="h-7 w-7 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Vibetune</h1>
              <p className="text-sm text-gray-400">Premium Music</p>
            </div>
          </div>
        </div>

        {/* Navigation Links */}
        <div className="px-4 py-6">
          {navigationItems.map((item) => (
            <Link
              key={item.title}
              to={item.url}
              className={`flex items-center px-4 py-3 mb-2 rounded-xl transition-colors ${
                location.pathname === item.url
                  ? 'bg-[#2a2b4a] text-white'
                  : 'text-gray-400 hover:text-white hover:bg-[#2a2b4a]'
              }`}
            > 
              <item.icon width={24} height={24} className="h-6 w-6 mr-3" />
              <span className="text-base">{item.title}</span>
            </Link>
          ))}
        </div>

        {/* User Profile */}
        <div className="p-4 mt-auto">
          <div className="bg-[#2a2b4a] rounded-xl p-4 flex items-center gap-3">
            <div className="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center">
              <UserCircleIcon width={24} height={24} className="h-6 w-6 text-white" />
            </div>
            <div>
              <p className="text-white font-medium">Music Lover</p>
              <p className="text-sm text-gray-400">Premium Member</p>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 ml-64 bg-white min-h-screen">
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
}