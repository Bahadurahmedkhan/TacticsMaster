# Railway Nixpacks Frontend Directory Fix

## Issue Resolved
Railway is now using Nixpacks (✅ "Using Nixpacks" in logs), but it's building from the root directory instead of the frontend directory, causing:
```
Could not find a required file.
Name: index.html
Searched in: /app/public
```

## Root Cause
Nixpacks is detecting the root `package.json` and trying to build from the root directory, but the React app files are in the `frontend/` directory.

## Solution Applied

### 1. Updated Root package.json
```json
{
  "name": "tactics-master-monorepo",
  "version": "1.0.0",
  "description": "Tactics Master - AI-powered cricket tactical analysis",
  "private": true,
  "scripts": {
    "build": "cd frontend && npm install && npm run build",
    "start": "cd frontend && serve -s build -l $PORT",
    "install": "cd frontend && npm install"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  },
  "workspaces": [
    "frontend"
  ]
}
```

### 2. Enhanced nixpacks.toml
```toml
[phases.setup]
nixPkgs = ["nodejs_18", "npm-9_x"]

[phases.install]
cmds = ["cd frontend && npm install"]

[phases.build]
cmds = ["cd frontend && npm run build"]

[start]
cmd = "cd frontend && serve -s build -l $PORT"

[providers]
node = "18"
```

### 3. Created .nixpacks Directory
- `.nixpacks/build.sh` - Custom build script
- `.nixpacks/start.sh` - Custom start script

### 4. Custom Build Script
```bash
#!/bin/bash
echo "Building frontend with Nixpacks..."
cd frontend
npm install
npm run build
npm install -g serve
echo "Build completed successfully!"
```

### 5. Custom Start Script
```bash
#!/bin/bash
echo "Starting frontend application..."
cd frontend
serve -s build -l $PORT
```

## Key Changes Made

1. **Root package.json**: Added workspaces and proper scripts
2. **Enhanced nixpacks.toml**: More specific configuration
3. **Custom Scripts**: `.nixpacks/build.sh` and `.nixpacks/start.sh`
4. **Frontend Navigation**: All commands navigate to frontend directory
5. **Multiple Fallbacks**: Root package.json, nixpacks.toml, and custom scripts

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
   - Railway will detect the root package.json
   - It will use Nixpacks with the enhanced configuration
   - Custom scripts will handle the frontend directory

4. **Set Environment Variables**
   ```
   REACT_APP_API_URL=https://tacticsmaster-production.up.railway.app
   GENERATE_SOURCEMAP=false
   NODE_ENV=production
   ```

5. **Deploy**
   - Click "Deploy"
   - Railway will use Nixpacks successfully

### Option 2: Railway CLI

1. **Navigate to Root Directory**
   ```bash
   cd /path/to/your/project
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
   railway variables set REACT_APP_API_URL=https://tacticsmaster-production.up.railway.app
   railway variables set GENERATE_SOURCEMAP=false
   railway variables set NODE_ENV=production
   ```

5. **Deploy**
   ```bash
   railway up
   ```

## Expected Build Process

### Using Enhanced Nixpacks:
1. Railway detects root package.json with workspaces
2. Uses enhanced nixpacks.toml configuration
3. Runs `cd frontend && npm install`
4. Runs `cd frontend && npm run build`
5. Starts with `cd frontend && serve -s build -l $PORT`

### Using Custom Scripts:
1. Railway runs `.nixpacks/build.sh`
2. Navigates to frontend directory
3. Installs dependencies and builds
4. Runs `.nixpacks/start.sh`
5. Serves the application

## Files Structure

```
├── package.json (root level - with workspaces)
├── nixpacks.toml (enhanced configuration)
├── .nixpacks/
│   ├── build.sh (custom build script)
│   └── start.sh (custom start script)
├── railway.toml (Railway configuration)
├── .railwayignore (ignores Dockerfiles)
└── frontend/
    ├── package.json
    ├── public/
    │   └── index.html
    └── src/
        └── ... (React app files)
```

## Troubleshooting

### If Nixpacks Still Builds from Root:
1. **Check Build Logs**: Look for "Using Nixpacks" and build commands
2. **Verify Scripts**: Ensure custom scripts are being used
3. **Check Workspaces**: Verify package.json workspaces configuration

### If Custom Scripts Fail:
1. **Check Script Permissions**: Ensure scripts are executable
2. **Verify Dependencies**: Check that all packages are in frontend/package.json
3. **Check Build Process**: Ensure the React app builds successfully

## Verification

After deployment:
1. Railway should show "Using Nixpacks" in build logs
2. Build should navigate to frontend directory
3. Find `index.html` in `frontend/public/`
4. Build the React app in `frontend/build/`
5. Serve static files with the `serve` package
6. Frontend accessible at Railway URL

## Alternative: Manual Override

If Nixpacks still builds from root:

1. **Go to Railway Dashboard**
2. **Select your service**
3. **Go to Settings**
4. **Set Build Command**: `cd frontend && npm install && npm run build`
5. **Set Start Command**: `cd frontend && serve -s build -l $PORT`

This comprehensive solution should force Nixpacks to build from the frontend directory and resolve all deployment issues!
