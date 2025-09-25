# Railway Frontend Deployment Fix

## Issue Resolved
The error `Could not find a required file. Name: index.html Searched in: /app/public` occurs because Railway is trying to build from the root directory instead of the `frontend` directory.

## Solution Applied

### 1. Created Railway Configuration Files

**Root Level (`railway.json`):**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd frontend && npm start",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Frontend Level (`frontend/railway.json`):**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm run build",
    "installCommand": "npm ci"
  },
  "deploy": {
    "startCommand": "serve -s build -l $PORT",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2. Added Nixpacks Configuration

**`frontend/nixpacks.toml`:**
```toml
[phases.setup]
nixPkgs = ["nodejs_18", "npm-9_x"]

[phases.install]
cmds = ["npm ci"]

[phases.build]
cmds = ["npm run build"]

[start]
cmd = "serve -s build -l $PORT"
```

### 3. Created Dockerfile

**`frontend/Dockerfile`:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
RUN npm install -g serve
EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]
```

### 4. Updated Dependencies

Added `serve` package to `package.json`:
```json
"serve": "^14.2.1"
```

## Deployment Steps

### Option 1: Railway Web Interface (Recommended)

1. **Go to Railway Dashboard**
   - Visit [railway.app](https://railway.app)
   - Login with your GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `Bahadurahmedkhan/TacticsMaster`

3. **Configure Service**
   - Railway will detect multiple services
   - **Select the `frontend` folder** as the service to deploy
   - Railway will automatically use the `frontend/railway.json` configuration

4. **Set Environment Variables**
   ```
   REACT_APP_API_URL=https://your-backend-url.railway.app
   GENERATE_SOURCEMAP=false
   NODE_ENV=production
   ```

5. **Deploy**
   - Click "Deploy"
   - Railway will build and deploy your frontend

### Option 2: Railway CLI

1. **Navigate to Frontend Directory**
   ```bash
   cd frontend
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Project**
   ```bash
   railway init
   ```

4. **Set Environment Variables**
   ```bash
   railway variables set REACT_APP_API_URL=https://your-backend-url.railway.app
   railway variables set GENERATE_SOURCEMAP=false
   railway variables set NODE_ENV=production
   ```

5. **Deploy**
   ```bash
   railway up
   ```

## Key Changes Made

1. **Fixed Build Context**: Railway now knows to build from the `frontend` directory
2. **Added Serve Package**: For serving static files in production
3. **Proper Configuration**: Multiple configuration files ensure Railway builds correctly
4. **Docker Support**: Added Dockerfile as fallback
5. **Nixpacks Configuration**: Explicit build commands for Railway

## Verification

After deployment, your frontend should be accessible at:
`https://your-frontend-name.railway.app`

## Troubleshooting

If you still encounter issues:

1. **Check Build Logs**: Look for any remaining errors in Railway dashboard
2. **Verify Environment Variables**: Ensure `REACT_APP_API_URL` is set correctly
3. **Test Locally**: Run `npm run build` in the frontend directory to ensure it builds
4. **Check Dependencies**: Ensure all packages are in `package.json`

## Files Created/Modified

- `railway.json` (root level)
- `frontend/railway.json` (updated)
- `frontend/nixpacks.toml` (new)
- `frontend/Dockerfile` (new)
- `frontend/package.json` (updated with serve package)
