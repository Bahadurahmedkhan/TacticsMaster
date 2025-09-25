# 🏏 Tactics Master - AI-Powered Cricket Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://langchain.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive AI-powered cricket analysis platform that provides intelligent tactical insights for coaches, analysts, and cricket enthusiasts. Built with LangChain's multi-tool agent architecture, the system orchestrates multiple specialized tools to deliver data-driven analysis, player assessments, and strategic recommendations.

## 🌟 Features

### 🧠 Multi-Agent Intelligence
- **Player Analysis**: Deep insights into individual player strengths, weaknesses, and tactical plans
- **Team Analysis**: Comprehensive squad assessment with strategic recommendations
- **Matchup Analysis**: Head-to-head records, venue factors, and historical trend analysis
- **Tactical Planning**: Advanced bowling plans, fielding strategies, and execution recommendations

### 🔧 Advanced Capabilities
- **Natural Language Processing**: Ask questions in plain English
- **Real-time Data Integration**: Live cricket data from multiple APIs
- **Pattern Recognition**: AI-powered identification of batting/bowling patterns
- **Statistical Analysis**: Advanced metrics and performance indicators
- **Contextual Intelligence**: Venue-specific, weather, and match-type considerations

### 🎨 Modern User Interface
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **Interactive Analysis**: Real-time query processing and results
- **Export Options**: Download analysis reports in multiple formats
- **Visual Analytics**: Charts and graphs for better data comprehension

## 🏗️ Architecture

### Backend Components
```
backend/
├── main.py                    # FastAPI application entry point
├── hybrid_agent.py           # Multi-tool agent implementation
├── tactics_master_agent.py   # Specialized cricket analysis agent
├── cricket_data_tool.py      # Cricket data API integration
├── tactical_analysis_tool.py # Tactical analysis engine
├── response_generation_tool.py # Response formatting
└── requirements.txt          # Python dependencies
```

### Frontend Components
```
frontend/
├── src/
│   ├── components/           # React components
│   │   ├── QueryInput.js    # Query interface
│   │   ├── AnalysisDisplay.js # Results display
│   │   ├── Header.js        # Navigation
│   │   └── LoadingSpinner.js # Loading states
│   ├── services/
│   │   └── api.js           # API communication
│   └── App.js               # Main application
├── package.json             # Node.js dependencies
└── tailwind.config.js       # Styling configuration
```

### Agent Tools
- **CricketDataTool**: Fetches live and historical cricket data
- **TacticalAnalysisTool**: Processes data for tactical insights
- **ResponseGenerationTool**: Formats analysis for coaches
- **HybridAgent**: Orchestrates multiple tools for complex analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- API Keys (see [API Setup Guide](API_SETUP_GUIDE.md))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Bahadurahmedkhan/TacticsMaster.git
   cd TacticsMaster
   ```

2. **Set up environment variables:**
   ```bash
   cp env_template .env
   # Edit .env with your API keys
   ```

3. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies:**
   ```bash
   cd ../frontend
   npm install
   ```

5. **Start the application:**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python main.py
   
   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

## 🔑 API Configuration

### Required API Keys

1. **Language Model API** (Choose one):
   - OpenAI API Key
   - Google Gemini API Key

2. **Cricket Data API** (Choose one):
   - CricAPI (Free tier available)
   - Sportmonks (Paid subscription)
   - ESPN Cricket API

### Environment Setup
```bash
# Copy the template
cp env_template .env

# Edit with your keys
GEMINI_API_KEY=your_gemini_api_key_here
CRICAPI_KEY=your_cricapi_key_here
```

## 📖 Usage Examples

### Player Analysis
```
Query: "Analyze Virat Kohli's weaknesses and create a bowling plan"
Context: Team: India, Opponent: Australia, Venue: MCG

Output:
- Overall assessment of player form
- Identified weaknesses (e.g., against spin, early innings)
- Specific bowling recommendations
- Fielding plan with key positions
- Tactical execution strategy
```

### Team Analysis
```
Query: "What are India's strengths against Australia?"
Context: Match Type: ODI, Venue: Narendra Modi Stadium

Output:
- Team performance assessment
- Key strengths and weaknesses
- Strategic recommendations
- Matchup-specific tactics
```

### Matchup Analysis
```
Query: "Give me a tactical plan for the upcoming match"
Context: Team: India, Opponent: Australia, Venue: MCG

Output:
- Historical performance analysis
- Venue-specific insights
- Key trends and patterns
- Strategic recommendations
```

## 🛠️ Development

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Linting
flake8 backend/
eslint frontend/src/

# Type checking
mypy backend/
```

### API Documentation
- Backend API: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## 🚀 Deployment

### Backend Deployment
```bash
# Using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# Using Docker
docker build -t tactics-master-backend .
docker run -p 8000:8000 tactics-master-backend
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Serve static files
npx serve -s build
```

### Environment Variables for Production
```bash
# Production environment
DEBUG=False
LOG_LEVEL=WARNING
GEMINI_API_KEY=your_production_key
CRICAPI_KEY=your_production_key
```

## 📊 API Endpoints

### POST `/analyze`
Analyze cricket tactics based on coach query.

**Request:**
```json
{
  "query": "Analyze Virat Kohli's weaknesses",
  "context": {
    "team": "India",
    "opponent": "Australia",
    "venue": "MCG",
    "matchType": "ODI"
  }
}
```

**Response:**
```json
{
  "response": "# 🏏 Tactical Analysis: Virat Kohli\n\n## 📊 Overall Assessment\n...",
  "analysis": {
    "player_analysis": {
      "overall_assessment": "Excellent form - key player in good touch",
      "key_insights": ["Vulnerable against spin bowling", "Dangerous in death overs"]
    }
  },
  "sources": ["Cricket Data API"]
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 🔮 Future Enhancements

- **Real-time Data Integration**: Live match data and updates
- **Advanced Analytics**: Machine learning models for prediction
- **Video Analysis**: Integration with video analysis tools
- **Team Collaboration**: Multi-user access and sharing
- **Mobile App**: Native mobile application
- **Voice Interface**: Voice-activated queries
- **Advanced Visualizations**: Interactive charts and graphs

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com) for the multi-tool agent framework
- [OpenAI](https://openai.com) and [Google Gemini](https://ai.google.dev) for language model capabilities
- [CricAPI](https://cricapi.com) and [Sportmonks](https://sportmonks.com) for cricket data
- The cricket community for inspiration and feedback

## 📞 Support

- 📧 Email: support@tacticsmaster.com
- 💬 Discord: [Join our community](https://discord.gg/tacticsmaster)
- 📖 Documentation: [docs.tacticsmaster.com](https://docs.tacticsmaster.com)
- 🐛 Issues: [GitHub Issues](https://github.com/Bahadurahmedkhan/TacticsMaster/issues)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Bahadurahmedkhan/TacticsMaster&type=Date)](https://star-history.com/#Bahadurahmedkhan/TacticsMaster&Date)

---

**Built with ❤️ for cricket coaches and analysts worldwide**

*Empowering cricket analysis through AI and modern technology*