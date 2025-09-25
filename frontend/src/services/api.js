import axios from 'axios';

/**
 * API service for communicating with the Tactics Master backend.
 * 
 * This module handles all HTTP requests to the backend API, including
 * analysis requests and health checks.
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Axios instance configured for the Tactics Master API.
 */
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout for analysis
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Request interceptor for logging API requests.
 */
api.interceptors.request.use(
  (config) => {
    console.log('Making API request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

/**
 * Response interceptor for handling API errors and logging.
 */
api.interceptors.response.use(
  (response) => {
    console.log('API response received:', response.status);
    return response;
  },
  (error) => {
    console.error('API error:', error.response?.data || error.message);
    
    // Handle different types of errors
    if (error.response?.status === 500) {
      throw new Error('Server error. Please try again later.');
    } else if (error.response?.status === 404) {
      throw new Error('Service not found. Please check if the backend is running.');
    } else if (error.code === 'ECONNABORTED') {
      throw new Error('Request timeout. The analysis is taking longer than expected.');
    } else if (!error.response) {
      throw new Error('Network error. Please check your connection and try again.');
    } else {
      throw new Error(error.response?.data?.detail || 'An unexpected error occurred.');
    }
  }
);

/**
 * Analyzes cricket tactics using the backend API.
 * 
 * @param {string} query - The cricket analysis query
 * @param {Object} context - Additional context for the analysis
 * @returns {Promise<Object>} Analysis results
 * @throws {Error} If the analysis request fails
 */
export const analyzeTactics = async (query, context = {}) => {
  try {
    const response = await api.post('/analyze', {
      query,
      context
    });
    
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Performs a health check on the backend API.
 * 
 * @returns {Promise<Object>} Health status information
 * @throws {Error} If the health check fails
 */
export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default api;
