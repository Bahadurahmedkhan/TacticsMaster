# Vercel Deployment Guide for Tactics Master

This guide will walk you through deploying both the frontend (React) and backend (FastAPI) of your Tactics Master application on Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Account**: Your code should be in a GitHub repository
3. **API Keys**: You'll need your Gemini API key and Cricket API key

## Step 1: Prepare Your Repository

### 1.1 Push Your Code to GitHub
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for Vercel deployment"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

## Step 2: Deploy the Backend (FastAPI)

### 2.1 Deploy Backend to Vercel

1. **Go to Vercel Dashboard**: Visit [vercel.com/dashboard](https://vercel.com/dashboard)
2. **Import Project**: Click "New Project" → "Import Git Repository"
3. **Select Repository**: Choose your GitHub repository
4. **Configure Backend**:
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
   - **Build Command**: Leave empty (Vercel will auto-detect)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

### 2.2 Set Environment Variables for Backend

In the Vercel dashboard for your backend project:

1. Go to **Settings** → **Environment Variables**
2. Add the following variables:
   ```
   GEMINI_API_KEY = your_actual_gemini_api_key
   CRICKET_API_KEY = your_actual_cricket_api_key
   CRICKET_API_BASE_URL = https://api.sportmonks.com/v3/football
   ```

### 2.3 Deploy Backend
- Click **Deploy**
- Wait for deployment to complete
- Note the backend URL (e.g., `https://your-backend-name.vercel.app`)

## Step 3: Deploy the Frontend (React)

### 3.1 Deploy Frontend to Vercel

1. **Create New Project**: In Vercel dashboard, click "New Project"
2. **Import Repository**: Select the same GitHub repository
3. **Configure Frontend**:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install`

### 3.2 Set Environment Variables for Frontend

In the Vercel dashboard for your frontend project:

1. Go to **Settings** → **Environment Variables**
2. Add the following variable:
   ```
   REACT_APP_API_URL = https://your-backend-name.vercel.app
   ```
   (Replace with your actual backend URL from Step 2.3)

### 3.3 Deploy Frontend
- Click **Deploy**
- Wait for deployment to complete
- Note the frontend URL (e.g., `https://your-frontend-name.vercel.app`)

## Step 4: Update CORS Settings (If Needed)

If you encounter CORS issues, update the backend CORS settings:

1. **Edit `backend/main.py`**:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:3000",  # React dev server
           "https://*.vercel.app",   # Vercel frontend domains
           "https://your-frontend-name.vercel.app",  # Your specific frontend domain
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Redeploy Backend**: Push changes and redeploy

## Step 5: Test Your Deployment

### 5.1 Test Backend
- Visit: `https://your-backend-name.vercel.app/docs`
- You should see the FastAPI documentation
- Test the `/health` endpoint

### 5.2 Test Frontend
- Visit: `https://your-frontend-name.vercel.app`
- Try submitting a cricket analysis query
- Check browser console for any errors

## Step 6: Custom Domain (Optional)

### 6.1 Add Custom Domain
1. Go to your project settings in Vercel
2. Navigate to **Domains**
3. Add your custom domain
4. Follow Vercel's DNS configuration instructions

## Troubleshooting

### Common Issues and Solutions

#### 1. CORS Errors
- **Problem**: Frontend can't connect to backend
- **Solution**: Update CORS settings in `backend/main.py` to include your Vercel domains

#### 2. Environment Variables Not Working
- **Problem**: API keys not being read
- **Solution**: Ensure environment variables are set in Vercel dashboard and redeploy

#### 3. Build Failures
- **Problem**: Frontend/backend won't build
- **Solution**: Check build logs in Vercel dashboard for specific errors

#### 4. 404 Errors
- **Problem**: Routes not found
- **Solution**: Ensure `vercel.json` files are correctly configured

### Debugging Steps

1. **Check Build Logs**: In Vercel dashboard → Functions → View Function Logs
2. **Test API Endpoints**: Use tools like Postman or curl
3. **Check Browser Console**: Look for JavaScript errors
4. **Verify Environment Variables**: Ensure they're set correctly

## File Structure After Deployment

```
your-repo/
├── backend/
│   ├── vercel.json          # Vercel configuration
│   ├── main.py             # FastAPI app
│   ├── requirements.txt    # Python dependencies
│   └── ...                 # Other backend files
├── frontend/
│   ├── vercel.json         # Vercel configuration
│   ├── package.json        # Node dependencies
│   └── ...                 # React app files
└── VERCEL_DEPLOYMENT_GUIDE.md
```

## Environment Variables Summary

### Backend Environment Variables
```
GEMINI_API_KEY=your_gemini_api_key_here
CRICKET_API_KEY=your_cricket_api_key_here
CRICKET_API_BASE_URL=https://api.sportmonks.com/v3/football
```

### Frontend Environment Variables
```
REACT_APP_API_URL=https://your-backend-name.vercel.app
```

## Deployment URLs

After successful deployment, you'll have:
- **Frontend**: `https://your-frontend-name.vercel.app`
- **Backend**: `https://your-backend-name.vercel.app`
- **Backend API Docs**: `https://your-backend-name.vercel.app/docs`

## Next Steps

1. **Monitor Performance**: Use Vercel Analytics to monitor your app
2. **Set up Monitoring**: Consider adding error tracking (Sentry, etc.)
3. **Optimize**: Use Vercel's performance insights to optimize your app
4. **Scale**: Vercel automatically handles scaling for you

## Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **FastAPI on Vercel**: [vercel.com/docs/frameworks/fastapi](https://vercel.com/docs/frameworks/fastapi)
- **React on Vercel**: [vercel.com/docs/frameworks/react](https://vercel.com/docs/frameworks/react)

---

**Note**: Make sure to replace placeholder URLs and API keys with your actual values throughout this guide.
