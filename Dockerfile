# Use Node.js 18 Alpine image
FROM node:18-alpine

# Set working directory to frontend
WORKDIR /app/frontend

# Copy package files from frontend directory
COPY frontend/package*.json ./

# Install dependencies
RUN npm install --production

# Copy source code from frontend directory
COPY frontend/ .

# Build the application
RUN npm run build

# Install serve globally
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Start the application
CMD ["serve", "-s", "build", "-l", "3000"]
