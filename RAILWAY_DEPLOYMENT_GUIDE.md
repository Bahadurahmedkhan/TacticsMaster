# Railway Deployment Guide for Tactics Master

This guide will walk you through deploying your Tactics Master cricket analysis application on Railway. Railway is perfect for deploying both your FastAPI backend and can also handle your React frontend.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Account**: Your code should be in a GitHub repository
3. **API Keys**: Gemini API key and Cricket API key

## Architecture Options

### Option 1: Full Stack on Railway
```
Backend (FastAPI) → Railway
Frontend (React) → Railway (Static Site)
```

### Option 2: Backend on Railway + Frontend on Netlify
```
Backend (FastAPI) → Railway
Frontend (React) → Netlify
```

## Step 1: Prepare Your Repository

### 1.1 Push Your Code to GitHub
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for Railway deployment"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

## Step 2: Deploy Backend to Railway

### 2.1 Create Railway Project

1. **Go to Railway Dashboard**: Visit [railway.app/dashboard](https://railway.app/dashboard)
2. **Create New Project**: Click "New Project"
3. **Deploy from GitHub**: Select "Deploy from GitHub repo"
4. **Select Repository**: Choose your GitHub repository

### 2.2 Configure Backend Service

1. **Railway will auto-detect**: It should detect your `backend` folder
2. **If not detected**: 
   - Go to your project settings
   - Click on the service
   - Set **Root Directory** to `backend`

### 2.3 Set Environment Variables

In your Railway project dashboard:

1. Go to **Variables** tab
2. Add the following environment variables:

```
GEMINI_API_KEY=your_actual_gemini_api_key
CRICKET_API_KEY=your_actual_cricket_api_key
CRICKET_API_BASE_URL=https://api.cricketdata.org
```

### 2.4 Railway Auto-Configuration

Railway will automatically:
- Detect it's a Python project
- Install dependencies from `requirements.txt`
- Start the application with `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 2.5 Deploy Backend

1. **Railway will auto-deploy** when you push to your main branch
2. **Manual Deploy**: Click "Deploy" button if needed
3. **Note the Backend URL**: e.g., `https://your-backend-name.railway.app`

## Step 3: Deploy Frontend (Choose One Option)

### Option A: Deploy Frontend to Railway (Recommended)

#### 3.1 Add Frontend Service to Railway

1. **In your Railway project**: Click "New Service"
2. **Deploy from GitHub**: Select the same repository
3. **Configure Frontend**:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Start Command**: `npx serve -s build -l 3000`

#### 3.2 Set Frontend Environment Variables

```
REACT_APP_API_URL=https://your-backend-name.railway.app
```

#### 3.3 Deploy Frontend

1. **Railway will auto-deploy** the frontend
2. **Note the Frontend URL**: e.g., `https://your-frontend-name.railway.app`

### Option B: Deploy Frontend to Netlify

1. **Go to Netlify**: [netlify.com/dashboard](https://netlify.com/dashboard)
2. **New Site from Git**: Connect your GitHub repository
3. **Configure**:
   - **Base Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Publish Directory**: `frontend/build`
4. **Set Environment Variable**:
   ```
   REACT_APP_API_URL=https://your-backend-name.railway.app
   ```

## Step 4: Update CORS Settings

### 4.1 Edit `backend/main.py`

Update your CORS settings to include Railway domains:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "https://*.railway.app",  # Railway frontend domains
        "https://your-frontend-name.railway.app",  # Your specific frontend domain
        "https://*.netlify.app",  # If using Netlify for frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4.2 Redeploy Backend

Push changes and Railway will automatically redeploy.

## Step 5: Test Your Deployment

### 5.1 Test Backend
- Visit: `https://your-backend-name.railway.app/docs`
- You should see the FastAPI documentation
- Test the `/health` endpoint

### 5.2 Test Frontend
- Visit: `https://your-frontend-name.railway.app` (or Netlify URL)
- Try submitting a cricket analysis query
- Check browser console for any errors

## Step 6: Railway Configuration Files

### 6.1 Create `railway.json` (Optional)

Create a `railway.json` file in your project root:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 6.2 Backend `Procfile` (Alternative)

Create `backend/Procfile`:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Step 7: Environment Variables Summary

### Backend Environment Variables (Railway)
```
GEMINI_API_KEY=your_gemini_api_key_here
CRICKET_API_KEY=your_cricket_api_key_here
CRICKET_API_BASE_URL=https://api.cricketdata.org
```

### Frontend Environment Variables
```
REACT_APP_API_URL=https://your-backend-name.railway.app
```

## Step 8: Continuous Deployment

### 8.1 Automatic Deployments
Railway automatically redeploys when you push to your main branch.

### 8.2 Branch Deployments
- **Production**: Deploy from `main` branch
- **Preview**: Deploy from feature branches (optional)

## Step 9: Monitoring and Logs

### 9.1 Railway Dashboard
- **Metrics**: CPU, Memory, Network usage
- **Logs**: Real-time application logs
- **Deployments**: Deployment history and status

### 9.2 Health Monitoring
- **Health Checks**: Automatic health monitoring
- **Uptime**: Service availability tracking
- **Alerts**: Email notifications for failures

## Troubleshooting

### Common Issues and Solutions

#### 1. CORS Errors
- **Problem**: Frontend can't connect to backend
- **Solution**: Update CORS settings in `backend/main.py` to include Railway domains

#### 2. Environment Variables Not Working
- **Problem**: API keys not being read
- **Solution**: Ensure environment variables are set in Railway dashboard and redeploy

#### 3. Build Failures
- **Problem**: Backend/frontend won't build
- **Solution**: Check build logs in Railway dashboard for specific errors

#### 4. Port Issues
- **Problem**: Application not starting
- **Solution**: Ensure you're using `$PORT` environment variable in start command

### Debugging Steps

1. **Check Railway Logs**: In Railway dashboard → View deployment logs
2. **Test API Endpoints**: Use tools like Postman or curl
3. **Check Browser Console**: Look for JavaScript errors
4. **Verify Environment Variables**: Ensure they're set correctly
5. **Check Health Endpoint**: Visit `/health` endpoint

## Step 10: Custom Domain (Optional)

### 10.1 Add Custom Domain to Railway
1. Go to your service settings in Railway
2. Navigate to **Domains**
3. Add your custom domain
4. Follow Railway's DNS configuration instructions

## Step 11: Performance Optimization

### 11.1 Railway Optimizations
- **Auto-scaling**: Railway automatically scales based on traffic
- **CDN**: Global CDN for fast content delivery
- **Caching**: Built-in caching for static assets

### 11.2 Application Optimizations
- **Health Checks**: Implement proper health check endpoints
- **Error Handling**: Robust error handling and logging
- **Resource Management**: Optimize memory and CPU usage

## File Structure After Deployment

```
your-repo/
├── railway.json              # Railway configuration (optional)
├── backend/
│   ├── Procfile             # Railway start command (optional)
│   ├── main.py              # FastAPI app
│   ├── requirements.txt     # Python dependencies
│   └── ...                  # Other backend files
├── frontend/
│   ├── package.json         # Node dependencies
│   ├── src/                 # React app files
│   └── build/               # Built files (generated)
└── RAILWAY_DEPLOYMENT_GUIDE.md
```

## Deployment URLs

After successful deployment, you'll have:
- **Backend**: `https://your-backend-name.railway.app`
- **Frontend**: `https://your-frontend-name.railway.app` (or Netlify URL)
- **Backend API Docs**: `https://your-backend-name.railway.app/docs`

## Next Steps

1. **Monitor Performance**: Use Railway metrics to monitor your app
2. **Set up Alerts**: Configure email notifications for failures
3. **Optimize**: Use Railway's performance insights to optimize your app
4. **Scale**: Railway automatically handles scaling for you
5. **Custom Domain**: Add your own domain for professional deployment

## Support Resources

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **React Documentation**: [reactjs.org](https://reactjs.org)

---

**Note**: Make sure to replace placeholder URLs and API keys with your actual values throughout this guide.
