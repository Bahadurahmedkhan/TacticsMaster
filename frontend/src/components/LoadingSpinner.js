import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner = () => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative">
        <Loader2 className="h-12 w-12 text-cricket-600 animate-spin" />
        <div className="absolute inset-0 h-12 w-12 border-2 border-cricket-200 rounded-full"></div>
      </div>
      
      <div className="mt-4 text-center">
        <h3 className="text-lg font-medium text-gray-900">Analyzing Tactics</h3>
        <p className="text-sm text-gray-600 mt-1">
          Gathering data and generating insights...
        </p>
      </div>
      
      <div className="mt-4 flex space-x-1">
        <div className="w-2 h-2 bg-cricket-600 rounded-full animate-bounce"></div>
        <div className="w-2 h-2 bg-cricket-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
        <div className="w-2 h-2 bg-cricket-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
      </div>
    </div>
  );
};

export default LoadingSpinner;
