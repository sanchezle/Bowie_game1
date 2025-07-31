#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script's directory to ensure context for Docker build, git pull, etc.
cd "$SCRIPT_DIR"

# Define variables
IMAGE_NAME="bowiegame:latest"
CONTAINER_NAME="bowiegame"
HOST_PORT=5001
CONTAINER_PORT=5000

echo "Starting deployment for BowieGame Flask application..."

# Pull the latest changes from the repository (if in git repo)
if [ -d ".git" ]; then
    echo "Pulling latest changes from Git..."
    git pull
fi

# Rebuild the Docker image
echo "Rebuilding Docker image ${IMAGE_NAME} (no cache)..."
docker build --no-cache -t ${IMAGE_NAME} .

# Stop the old container if it's running
if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
    echo "Stopping existing container ${CONTAINER_NAME}..."
    docker stop ${CONTAINER_NAME}
fi

# Remove the old container if it exists
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "Removing existing container ${CONTAINER_NAME}..."
    docker rm ${CONTAINER_NAME}
fi

# Create environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file template..."
    cat > .env << 'EOF'
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=production

# OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FACEBOOK_CLIENT_ID=your-facebook-client-id
FACEBOOK_CLIENT_SECRET=your-facebook-client-secret

# Email Configuration
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=your-email@domain.com

# Database Configuration
DATABASE_URL=sqlite:///bowiegame.db
EOF
    echo "⚠️  Please edit .env file with your actual configuration values!"
fi

# Run a new container with the updated image
echo "Running new container ${CONTAINER_NAME}..."
docker run -d --name ${CONTAINER_NAME} \
  -p ${HOST_PORT}:${CONTAINER_PORT} \
  --env-file .env \
  -e SECRET_KEY="$(openssl rand -hex 32)" \
  -v "$(pwd)/bowiegame.db:/app/bowiegame.db" \
  -v "$(pwd)/flask_session:/app/flask_session" \
  --restart unless-stopped \
  ${IMAGE_NAME}

echo "Deployment complete. BowieGame should be running."
echo "Container ${CONTAINER_NAME} is running on port ${HOST_PORT}"
echo "Access it locally at: http://localhost:${HOST_PORT}"
echo ""
echo "🎮 BowieGame: Ready for nginx proxy integration"
echo "🔧 Configure nginx to proxy /projects/bowiegame to localhost:${HOST_PORT}"
echo ""
echo "Container logs: docker logs -f ${CONTAINER_NAME}"
echo "Container status: docker ps | grep ${CONTAINER_NAME}"