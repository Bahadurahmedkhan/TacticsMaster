# Railway Backend Deployment Settings

## 🚀 Railway Backend Configuration Commands

### **Step 1: Railway Project Setup**

1. **Go to Railway Dashboard**: [railway.app/dashboard](https://railway.app/dashboard)
2. **Create New Project**: Click "New Project"
3. **Deploy from GitHub**: Select "Deploy from GitHub repo"
4. **Select Repository**: Choose `Bahadurahmedkhan/TacticsMaster`

### **Step 2: Backend Service Configuration**

#### **Service Settings:**
- **Service Name**: `tactics-master-backend`
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### **Alternative Start Commands (if needed):**
```bash
# Option 1: Standard uvicorn
uvicorn main:app --host 0.0.0.0 --port $PORT

# Option 2: With workers
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1

# Option 3: With reload disabled (production)
uvicorn main:app --host 0.0.0.0 --port $PORT --reload false

# Option 4: Using Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### **Step 3: Environment Variables**

Set these environment variables in Railway dashboard:

```bash
# Required API Keys
GEMINI_API_KEY=your_actual_gemini_api_key_here
CRICKET_API_KEY=your_actual_cricket_api_key_here
CRICKET_API_BASE_URL=https://api.cricketdata.org

# Optional: Python Version (if not using .python-version file)
PYTHON_VERSION=3.11

# Optional: Debug Settings
DEBUG=False
LOG_LEVEL=INFO
```

### **Step 4: Build Configuration**

#### **Build Commands:**
```bash
# Primary build command
pip install -r requirements.txt

# Alternative with upgrade
pip install --upgrade -r requirements.txt

# With specific Python version
python3.11 -m pip install -r requirements.txt
```

#### **Build Environment Variables:**
```bash
# Python version
PYTHON_VERSION=3.11

# Build optimization
PIP_NO_CACHE_DIR=1
PIP_DISABLE_PIP_VERSION_CHECK=1
```

### **Step 5: Health Check Configuration**

#### **Health Check Settings:**
- **Health Check Path**: `/health`
- **Health Check Timeout**: `100` seconds
- **Health Check Interval**: `30` seconds

#### **Health Check Commands:**
```bash
# Test health endpoint
curl -f https://your-backend-name.railway.app/health

# Test with timeout
curl -f --max-time 30 https://your-backend-name.railway.app/health
```

### **Step 6: CORS Configuration**

Update your `backend/main.py` CORS settings:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "https://*.railway.app",  # Railway frontend domains
        "https://*.netlify.app",  # Netlify frontend domains
        "https://your-frontend-name.railway.app",  # Your specific frontend domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Step 7: Railway-Specific Commands**

#### **Railway CLI Commands (if using Railway CLI):**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to project
railway link

# Deploy
railway up

# View logs
railway logs

# Set environment variables
railway variables set GEMINI_API_KEY=your_key
railway variables set CRICKET_API_KEY=your_key
```

#### **Manual Deployment Commands:**
```bash
# Test locally first
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Test with production settings
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1 --reload false
```

### **Step 8: Monitoring Commands**

#### **Check Deployment Status:**
```bash
# Check if service is running
curl -f https://your-backend-name.railway.app/health

# Check API documentation
curl -f https://your-backend-name.railway.app/docs

# Test analyze endpoint
curl -X POST https://your-backend-name.railway.app/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Test query", "context": {}}'
```

#### **Debug Commands:**
```bash
# Check Railway logs
railway logs --follow

# Check service status
railway status

# View environment variables
railway variables
```

### **Step 9: Production Optimization**

#### **Production Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

#### **Performance Settings:**
```bash
# Environment variables for production
WORKERS=4
MAX_REQUESTS=1000
MAX_REQUESTS_JITTER=100
TIMEOUT_KEEP_ALIVE=5
```

### **Step 10: Troubleshooting Commands**

#### **Common Issues and Solutions:**

**1. Build Failures:**
```bash
# Check build logs
railway logs --build

# Test requirements locally
pip install -r requirements.txt
```

**2. Import Errors:**
```bash
# Test imports locally
cd backend
python -c "from main import app; print('✅ App imports successfully')"
```

**3. Port Issues:**
```bash
# Test with Railway port
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**4. Environment Variables:**
```bash
# Check environment variables
railway variables

# Set missing variables
railway variables set GEMINI_API_KEY=your_key
```

## 📋 **Complete Railway Backend Settings Summary**

### **Required Settings:**
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path**: `/health`

### **Required Environment Variables:**
```
GEMINI_API_KEY=your_actual_gemini_api_key
CRICKET_API_KEY=your_actual_cricket_api_key
CRICKET_API_BASE_URL=https://api.cricketdata.org
```

### **Optional Settings:**
```
PYTHON_VERSION=3.11
DEBUG=False
LOG_LEVEL=INFO
WORKERS=1
```

## 🎯 **Quick Deployment Checklist**

- [ ] Repository connected to Railway
- [ ] Root directory set to `backend`
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Environment variables set
- [ ] Health check path: `/health`
- [ ] CORS settings updated
- [ ] Deploy and test

## 🔗 **After Deployment:**

- **Backend URL**: `https://your-backend-name.railway.app`
- **API Docs**: `https://your-backend-name.railway.app/docs`
- **Health Check**: `https://your-backend-name.railway.app/health`
- **Analyze Endpoint**: `https://your-backend-name.railway.app/analyze`
