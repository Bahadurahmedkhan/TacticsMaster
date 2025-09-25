# Use Node.js 18 Alpine image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy all files (including frontend directory)
COPY . .

# Navigate to frontend directory and install dependencies
RUN cd frontend && npm install --production

# Build the application
RUN cd frontend && npm run build

# Install serve globally
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Start the application
CMD ["serve", "-s", "frontend/build", "-l", "3000"]
