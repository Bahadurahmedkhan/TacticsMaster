import React, { useState, useCallback } from 'react';
import { Send, Target, Users, TrendingUp } from 'lucide-react';

/**
 * QueryInput component for handling user input and context for cricket analysis.
 * 
 * This component provides a form interface for users to enter their analysis queries
 * and provide additional context like team, opponent, venue, and match type.
 * 
 * @component
 * @param {Object} props - Component props
 * @param {Function} props.onAnalyze - Callback function when analysis is requested
 * @param {Function} props.onClear - Callback function to clear the form
 * @returns {JSX.Element} The QueryInput component
 */
const QueryInput = ({ onAnalyze, onClear }) => {
  // Form state
  const [query, setQuery] = useState('');
  const [context, setContext] = useState({
    team: '',
    opponent: '',
    venue: '',
    matchType: 'ODI'
  });

  /**
   * Handles form submission for analysis requests.
   * 
   * @param {Event} e - Form submit event
   */
  const handleSubmit = useCallback((e) => {
    e.preventDefault();
    if (query.trim()) {
      onAnalyze(query.trim(), context);
    }
  }, [query, context, onAnalyze]);

  /**
   * Clears the form and resets all fields to default values.
   */
  const handleClear = useCallback(() => {
    setQuery('');
    setContext({
      team: '',
      opponent: '',
      venue: '',
      matchType: 'ODI'
    });
    onClear();
  }, [onClear]);

  /**
   * Example queries to help users get started.
   */
  const exampleQueries = [
    "Analyze Virat Kohli's weaknesses and create a bowling plan",
    "What are India's strengths against Australia?",
    "Give me a tactical plan for the upcoming match",
    "Analyze the opponent's batting lineup"
  ];

  /**
   * Handles clicking on example queries to populate the form.
   * 
   * @param {string} exampleQuery - The example query to set
   */
  const handleExampleClick = useCallback((exampleQuery) => {
    setQuery(exampleQuery);
  }, []);

  /**
   * Handles changes to context fields.
   * 
   * @param {string} field - The field name to update
   * @param {string} value - The new value
   */
  const handleContextChange = useCallback((field, value) => {
    setContext(prev => ({
      ...prev,
      [field]: value
    }));
  }, []);

  return (
    <div className="bg-slate-800/60 backdrop-blur-sm rounded-lg shadow-lg border border-cyan-500/20 p-6 mb-6">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-white mb-2">
          Cricket Tactical Analysis
        </h2>
        <p className="text-cyan-300">
          Ask me anything about cricket tactics, player analysis, or match strategy.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="query" className="block text-sm font-medium text-cyan-300 mb-2">
            Your Query
          </label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., Analyze Virat Kohli's weaknesses and create a bowling plan against him"
            className="w-full px-4 py-3 bg-slate-700/50 border border-cyan-500/30 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 resize-none text-white placeholder-gray-400"
            rows={3}
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label htmlFor="team" className="block text-sm font-medium text-cyan-300 mb-1">
              Your Team
            </label>
            <input
              type="text"
              id="team"
              value={context.team}
              onChange={(e) => handleContextChange('team', e.target.value)}
              placeholder="e.g., India"
              className="w-full px-3 py-2 bg-slate-700/50 border border-cyan-500/30 rounded-md focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 text-white placeholder-gray-400"
            />
          </div>

          <div>
            <label htmlFor="opponent" className="block text-sm font-medium text-cyan-300 mb-1">
              Opponent
            </label>
            <input
              type="text"
              id="opponent"
              value={context.opponent}
              onChange={(e) => handleContextChange('opponent', e.target.value)}
              placeholder="e.g., Australia"
              className="w-full px-3 py-2 bg-slate-700/50 border border-cyan-500/30 rounded-md focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 text-white placeholder-gray-400"
            />
          </div>

          <div>
            <label htmlFor="venue" className="block text-sm font-medium text-cyan-300 mb-1">
              Venue
            </label>
            <input
              type="text"
              id="venue"
              value={context.venue}
              onChange={(e) => handleContextChange('venue', e.target.value)}
              placeholder="e.g., MCG"
              className="w-full px-3 py-2 bg-slate-700/50 border border-cyan-500/30 rounded-md focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 text-white placeholder-gray-400"
            />
          </div>

          <div>
            <label htmlFor="matchType" className="block text-sm font-medium text-cyan-300 mb-1">
              Match Type
            </label>
            <select
              id="matchType"
              value={context.matchType}
              onChange={(e) => handleContextChange('matchType', e.target.value)}
              className="w-full px-3 py-2 bg-slate-700/50 border border-cyan-500/30 rounded-md focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 text-white"
            >
              <option value="ODI">ODI</option>
              <option value="T20">T20</option>
              <option value="Test">Test</option>
            </select>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <button
            type="submit"
            disabled={!query.trim()}
            className="flex items-center justify-center px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-lg hover:from-cyan-400 hover:to-blue-400 disabled:bg-gray-600 disabled:cursor-not-allowed transition-all duration-300 shadow-lg shadow-cyan-500/30"
          >
            <Send className="h-5 w-5 mr-2" />
            Analyze Tactics
          </button>

          <button
            type="button"
            onClick={handleClear}
            className="flex items-center justify-center px-6 py-3 bg-slate-600 text-white rounded-lg hover:bg-slate-500 transition-colors"
          >
            Clear
          </button>
        </div>
      </form>

      <div className="mt-6">
        <h3 className="text-sm font-medium text-cyan-300 mb-3">Example Queries:</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {exampleQueries.map((example, index) => (
            <button
              key={index}
              onClick={() => handleExampleClick(example)}
              className="text-left p-3 text-sm text-cyan-200 bg-slate-700/50 rounded-lg hover:bg-slate-600/50 transition-colors border border-cyan-500/20"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default QueryInput;
