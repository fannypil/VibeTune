import React, { useState } from "react";
import { Disc3 } from "lucide-react";
import Login from "../components/login";
import Register from "../components/register";

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
      <div className="max-w-6xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left side - Hero content */}
          <div className="text-center lg:text-left">
            <div className="flex items-center justify-center lg:justify-start gap-4 mb-8">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-2xl">
                <Disc3 className="w-10 h-10 text-white" />
              </div>
              <div>
                <h1 className="text-4xl font-bold text-white tracking-tight">VibeTune</h1>
                <p className="text-purple-200 font-medium">AI-Powered Music Experience</p>
              </div>
            </div>

            <h2 className="text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
              Your Music Journey Starts Here
            </h2>
            <p className="text-xl text-purple-200 mb-8">
              Join VibeTune to discover personalized playlists powered by AI
            </p>
          </div>

          {/* Right side - Auth forms */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl">
            {isLogin ? (
              <Login onSwitchToRegister={() => setIsLogin(false)} />
            ) : (
              <Register onSwitchToLogin={() => setIsLogin(true)} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}