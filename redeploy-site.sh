#!/bin/bash

# Killing all existing tmux sessions
tmux kill-server

# Navigating to the project folder
cd ~/Portfolio-Site-MLH

# Ensuring that the git repository has the latest changes from the main branch
git fetch && git reset origin/main --hard

# Python virtual environment and install dependencies
source ~/Portfolio-Site-MLH/python3-virtualenv/bin/activate
pip install -r requirements.txt
deactivate

# Start a new detached Tmux session
tmux new-session -d -s flask_app "cd ~/Portfolio-Site-MLH && source ~/Portfolio-Site-MLH/python3-virtualenv/bin/activate && flask run --host=0.0.0.0"

echo "Deployment script executed successfully."
