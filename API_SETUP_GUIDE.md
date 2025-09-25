# 🔑 API Setup Guide for Tactics Master

This guide will help you set up the necessary API keys for the Tactics Master agent to work with real cricket data and language models.

## 🤖 Language Model APIs

### Option 1: OpenAI API (Recommended)
1. **Sign up**: Go to [OpenAI Platform](https://platform.openai.com/)
2. **Get API Key**: Navigate to API Keys section and create a new key
3. **Add to .env**: Set `OPENAI_API_KEY=your_key_here`
4. **Cost**: Pay-per-use, starts with $5 free credit

### Option 2: Google Gemini API
1. **Sign up**: Go to [Google AI Studio](https://aistudio.google.com/)
2. **Get API Key**: Create a new API key in the API Keys section
3. **Add to .env**: Set `GEMINI_API_KEY=your_key_here`
4. **Cost**: Free tier available with usage limits

## 🏏 Cricket Data APIs

### Option 1: CricAPI (Free Tier Available)
1. **Sign up**: Go to [CricAPI](https://cricapi.com/)
2. **Get API Key**: Register and get your free API key
3. **Add to .env**: Set `CRICAPI_KEY=your_key_here`
4. **Limits**: 100 requests/day on free tier
5. **Features**: Player stats, match data, live scores

### Option 2: Sportmonks (Paid)
1. **Sign up**: Go to [Sportmonks](https://www.sportmonks.com/)
2. **Choose Plan**: Select a subscription plan
3. **Get API Key**: Access your API key from dashboard
4. **Add to .env**: Set `CRICKET_API_KEY=your_key_here`
5. **Features**: Comprehensive cricket data, 140+ leagues

### Option 3: ESPN Cricket API (Free)
1. **No signup required**: ESPN Cricket API is free
2. **Add to .env**: Set `ESPN_CRICKET_API_KEY=free` (or leave empty)
3. **Limits**: Rate limited but free
4. **Features**: Basic match data and scores

## 🚀 Quick Setup

### Minimal Setup (Free)
```bash
# Copy environment template
cp env_template .env

# Edit .env file with your keys
OPENAI_API_KEY=your_openai_key_here
CRICAPI_KEY=your_cricapi_key_here
```

### Full Setup (Paid)
```bash
# Copy environment template
cp env_template .env

# Edit .env file with all keys
OPENAI_API_KEY=your_openai_key_here
CRICKET_API_KEY=your_sportmonks_key_here
CRICAPI_KEY=your_cricapi_key_here
```

## 🔧 Testing Your Setup

### Test Language Model
```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

if os.getenv('OPENAI_API_KEY'):
    print('✅ OpenAI API key found')
elif os.getenv('GEMINI_API_KEY'):
    print('✅ Gemini API key found')
else:
    print('❌ No language model API key found')
"
```

### Test Cricket API
```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

if os.getenv('CRICAPI_KEY'):
    print('✅ CricAPI key found')
if os.getenv('CRICKET_API_KEY'):
    print('✅ Sportmonks API key found')
if not os.getenv('CRICAPI_KEY') and not os.getenv('CRICKET_API_KEY'):
    print('⚠️  No cricket API keys found - will use mock data')
"
```

## 💡 Recommendations

### For Development/Testing
- **Language Model**: Use Gemini (free tier)
- **Cricket Data**: Use CricAPI (free tier)
- **Total Cost**: $0

### For Production
- **Language Model**: Use OpenAI (better performance)
- **Cricket Data**: Use Sportmonks (comprehensive data)
- **Total Cost**: ~$20-50/month depending on usage

### For Maximum Features
- **Language Model**: OpenAI
- **Cricket Data**: Both CricAPI + Sportmonks
- **Fallback**: ESPN Cricket API
- **Total Cost**: ~$30-60/month

## 🛠️ Troubleshooting

### Common Issues

1. **"No API key found"**
   - Check your .env file exists
   - Verify API key is correctly set
   - Restart the application

2. **"API rate limit exceeded"**
   - Wait for rate limit to reset
   - Consider upgrading to paid plan
   - Use mock data for development

3. **"Invalid API key"**
   - Verify key is correct
   - Check for extra spaces
   - Regenerate key if needed

### Getting Help

- Check the [README.md](README.md) for setup instructions
- Review the [API documentation](https://docs.cricapi.com/) for cricket APIs
- Check [OpenAI documentation](https://platform.openai.com/docs) for language model issues

## 📊 API Usage Tracking

### Monitor Your Usage
- **OpenAI**: Check usage in [OpenAI Dashboard](https://platform.openai.com/usage)
- **Gemini**: Check usage in [Google AI Studio](https://aistudio.google.com/)
- **CricAPI**: Check usage in [CricAPI Dashboard](https://cricapi.com/myaccount)
- **Sportmonks**: Check usage in [Sportmonks Dashboard](https://www.sportmonks.com/myaccount)

### Cost Optimization
- Use free tiers for development
- Implement caching to reduce API calls
- Use mock data for testing
- Monitor usage regularly

---

**Ready to start?** Run `python app/main.py` after setting up your API keys!
