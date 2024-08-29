#!/bin/bash

# Define variables
SERVICE_NAME="docker-service-api"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
PROJECT_DIR="/home/ubuntu/flwr-docker-service-api"
LOCAL_SERVICE_FILE="$PROJECT_DIR/$SERVICE_NAME.service"

# Check if the service file exists in the project directory
if [ ! -f "$LOCAL_SERVICE_FILE" ]; then
    echo "Service file $LOCAL_SERVICE_FILE not found!"
    exit 1
fi

# Copy the service file to the systemd directory
echo "Copying service file to systemd directory..."
sudo cp "$LOCAL_SERVICE_FILE" "$SERVICE_FILE"

# Reload systemd to recognize the new service
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Restart the service
echo "Restarting the $SERVICE_NAME service..."
sudo systemctl restart "$SERVICE_NAME"

# Enable the service to start on boot (if not already enabled)
echo "Enabling the $SERVICE_NAME service to start on boot..."
sudo systemctl enable "$SERVICE_NAME"

# Check the status of the service
echo "Checking the status of the $SERVICE_NAME service..."
sudo systemctl status "$SERVICE_NAME"
