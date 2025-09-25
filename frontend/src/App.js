import React, { useState, useCallback } from 'react';
import Header from './components/Header';
import QueryInput from './components/QueryInput';
import AnalysisDisplay from './components/AnalysisDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import WelcomePage from './components/WelcomePage';
import About from './components/About';
import { analyzeTactics } from './services/api';

/**
 * Main App component for the Tactics Master cricket analysis application.
 * 
 * This component manages the overall application state and routing between
 * different views (welcome, analysis, about).
 * 
 * @component
 * @returns {JSX.Element} The main application component
 */
function App() {
  // State management
  const [showWelcome, setShowWelcome] = useState(true);
  const [showAbout, setShowAbout] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);

  /**
   * Handles the analysis request from the user.
   * 
   * @param {string} query - The user's analysis query
   * @param {Object} context - Additional context for the analysis
   */
  const handleAnalyze = useCallback(async (query, context = {}) => {
    if (!query || !query.trim()) {
      setError('Please enter a valid query for analysis.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const result = await analyzeTactics(query, context);
      setAnalysis(result);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message || 'An error occurred while analyzing your query');
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Clears the current analysis and error states.
   */
  const handleClear = useCallback(() => {
    setAnalysis(null);
    setError(null);
  }, []);

  /**
   * Handles navigation to the main analysis interface.
   */
  const handleGetStarted = useCallback(() => {
    setShowWelcome(false);
  }, []);

  /**
   * Handles navigation back to the welcome page.
   */
  const handleBackToWelcome = useCallback(() => {
    setShowWelcome(true);
    setShowAbout(false);
  }, []);

  /**
   * Toggles the about page visibility.
   */
  const handleAboutClick = useCallback(() => {
    setShowAbout(prev => !prev);
  }, []);

  /**
   * Handles navigation back to the analysis interface from about page.
   */
  const handleBackToAnalysis = useCallback(() => {
    setShowAbout(false);
  }, []);

  // Render welcome page if user hasn't started
  if (showWelcome) {
    return <WelcomePage onGetStarted={handleGetStarted} />;
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
        <div className="absolute -top-1/4 -left-1/4 w-1/2 h-1/2 bg-cyan-500/10 rounded-full filter blur-[200px]"></div>
        <div className="absolute -bottom-1/4 -right-1/4 w-1/2 h-1/2 bg-indigo-600/10 rounded-full filter blur-[200px]"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-400/5 rounded-full filter blur-[300px]"></div>
      </div>
      
      <div className="relative z-10">
        <Header 
          onBackToWelcome={handleBackToWelcome} 
          onAboutClick={handleAboutClick} 
          showAbout={showAbout} 
        />
        
        {!showAbout && (
          <main className="container mx-auto px-4 py-8">
            <div className="max-w-4xl mx-auto">
              <QueryInput onAnalyze={handleAnalyze} onClear={handleClear} />
              
              {isLoading && <LoadingSpinner />}
              
              {error && (
                <div className="mt-6 p-4 bg-red-900/20 border border-red-500/30 rounded-lg backdrop-blur-sm">
                  <div className="flex items-center">
                    <div className="text-red-400 font-medium">Error:</div>
                    <div className="ml-2 text-red-300">{error}</div>
                  </div>
                </div>
              )}
              
              {analysis && <AnalysisDisplay analysis={analysis} />}
            </div>
          </main>
        )}
        
        {showAbout && <About onBackToAnalysis={handleBackToAnalysis} />}
      </div>
    </div>
  );
}

export default App;
