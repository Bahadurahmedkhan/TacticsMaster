#!/usr/bin/env node

const { execSync } = require('child_process');
const path = require('path');

console.log('🚀 Building frontend with custom script...');

try {
  // Navigate to frontend directory
  process.chdir(path.join(__dirname, 'frontend'));
  
  console.log('📦 Installing dependencies...');
  execSync('npm install', { stdio: 'inherit' });
  
  console.log('🔨 Building React app...');
  execSync('npm run build', { stdio: 'inherit' });
  
  console.log('📦 Installing serve globally...');
  execSync('npm install -g serve', { stdio: 'inherit' });
  
  console.log('✅ Build completed successfully!');
  console.log('🚀 Starting server...');
  
  // Start the server
  execSync('serve -s build -l $PORT', { stdio: 'inherit' });
  
} catch (error) {
  console.error('❌ Build failed:', error.message);
  process.exit(1);
}
