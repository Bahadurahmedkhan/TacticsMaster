# Frontend Railway Deployment Guide

This guide will walk you through deploying the Tactics Master frontend to Railway.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Railway CLI**: Install the Railway CLI
3. **Node.js**: Ensure Node.js 16+ is installed
4. **Backend Deployed**: Your backend should already be deployed on Railway

## Step-by-Step Deployment

### Step 1: Install Railway CLI

**For Windows:**
```bash
npm install -g @railway/cli
```

**For macOS/Linux:**
```bash
npm install -g @railway/cli
```

### Step 2: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 3: Login to Railway

```bash
railway login
```

### Step 4: Create New Railway Project

```bash
railway init
```

This will:
- Create a new Railway project
- Generate a `railway.json` configuration file
- Set up the project structure

### Step 5: Configure Environment Variables

Set the following environment variables in Railway dashboard or via CLI:

```bash
# Set your backend URL (replace with your actual backend URL)
railway variables set REACT_APP_API_URL=https://your-backend-url.railway.app

# Production settings
railway variables set GENERATE_SOURCEMAP=false
railway variables set NODE_ENV=production
```

### Step 6: Configure Build Settings

Railway will automatically detect this as a React app and:
- Install dependencies with `npm install`
- Build the app with `npm run build`
- Serve the static files

### Step 7: Deploy

```bash
railway up
```

### Step 8: Get Your Frontend URL

After deployment, Railway will provide you with a URL like:
`https://your-frontend-name.railway.app`

## Alternative: Using the Deployment Scripts

### For Windows:
```bash
deploy-to-railway.bat
```

### For macOS/Linux:
```bash
chmod +x deploy-to-railway.sh
./deploy-to-railway.sh
```

## Configuration Files

The following files have been created for Railway deployment:

1. **`railway.json`**: Railway configuration
2. **`Procfile`**: Process definition
3. **`package-railway.json`**: Production package configuration
4. **`env.production`**: Production environment variables
5. **`deploy-to-railway.sh/.bat`**: Deployment scripts

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `https://your-backend.railway.app` |
| `GENERATE_SOURCEMAP` | Disable source maps in production | `false` |
| `NODE_ENV` | Environment mode | `production` |

## Troubleshooting

### Common Issues:

1. **Build Failures**: Check that all dependencies are in `package.json`
2. **API Connection Issues**: Verify `REACT_APP_API_URL` is correct
3. **Static File Serving**: Ensure `serve` package is included

### Debug Commands:

```bash
# Check Railway status
railway status

# View logs
railway logs

# Check environment variables
railway variables
```

## Production Checklist

- [ ] Backend is deployed and accessible
- [ ] Environment variables are set correctly
- [ ] Build completes successfully
- [ ] Frontend loads without errors
- [ ] API calls work correctly
- [ ] All features are functional

## Custom Domain (Optional)

To use a custom domain:

1. Go to your Railway project dashboard
2. Navigate to Settings > Domains
3. Add your custom domain
4. Configure DNS records as instructed

## Monitoring

Railway provides built-in monitoring:
- View logs in the Railway dashboard
- Monitor performance metrics
- Set up alerts for downtime

## Cost Considerations

Railway offers:
- Free tier with limited usage
- Pay-as-you-go pricing
- Automatic scaling

Check [Railway Pricing](https://railway.app/pricing) for current rates.

## Security Notes

- Never commit `.env` files with sensitive data
- Use Railway's environment variables for secrets
- Enable HTTPS (automatic with Railway)
- Regularly update dependencies

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- GitHub Issues: Create an issue in your repository
