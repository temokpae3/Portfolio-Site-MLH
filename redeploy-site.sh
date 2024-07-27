#!/bin/bash

# Navigating to the project folder
cd ~/Portfolio-Site-MLH

# Ensuring that the git repository has the latest changes from the main branch
git fetch && git reset origin/main --hard

# Python virtual environment and install dependencies
source ~/Portfolio-Site-MLH/python3-virtualenv/bin/activate
pip install -r requirements.txt
deactivate

# Restart the service
docker compose -f docker-compose.prod.yml down

docker compose -f docker-compose.prod.yml up -d --build

echo "Deployment script executed successfully."
