import React from 'react';
import { Target } from 'lucide-react';

const Header = ({ onBackToWelcome, onAboutClick, showAbout }) => {
  return (
    <header className="bg-slate-900/95 backdrop-blur-sm border-b border-cyan-500/20 shadow-lg shadow-cyan-500/10">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <button 
            onClick={onBackToWelcome}
            className="flex items-center space-x-3 hover:opacity-80 transition-opacity duration-300"
          >
            <div className="p-2 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg">
              <Target className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-white bg-clip-text text-transparent">
                Tactics Master
              </h1>
              <p className="text-sm text-cyan-300">AI-Powered Cricket Analysis</p>
            </div>
          </button>
          
          <div className="flex items-center space-x-4">
            <div className="hidden md:flex items-center space-x-6">
              <button 
                onClick={onAboutClick}
                className={`px-4 py-2 rounded-lg transition-all duration-300 ${
                  showAbout 
                    ? 'bg-cyan-500 text-white' 
                    : 'text-cyan-300 hover:text-white hover:bg-cyan-500/20'
                }`}
              >
                About
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
