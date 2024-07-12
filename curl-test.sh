#!/bin/bash

# Base URL of theFlask application
BASE_URL="http://localhost:5000/api"

# Data for creating a timeline post
NAME="Test User"
EMAIL="test@example.com"
CONTENT="This is a test timeline post created at $(date)"

# Function to send a POST request to create a timeline post
create_timeline_post() {
    echo "Creating timeline post:"
    echo "Name: $NAME"
    echo "Email: $EMAIL"
    echo "Content: $CONTENT"

    curl -X POST \
        "$BASE_URL/timeline_post" \
        -d "name=$NAME&email=$EMAIL&content=$CONTENT"
}

# Function to send a GET request to retrieve all timeline posts
get_timeline_posts() {
    echo "Getting timeline posts:"
    curl -X GET "$BASE_URL/timeline_post"
}

# Function to send a DELETE request to delete a specific timeline post
delete_timeline_post() {
    local post_id=$1

    echo "Deleting timeline post with ID: $post_id"
    curl -X DELETE "$BASE_URL/timeline_post/$post_id"
}

# Main script
echo "Testing Timeline Post API endpoints"

# Creating a timeline post
create_timeline_post

# Wait for a few seconds to ensure the post is added
sleep 10

# Get all timeline posts
get_timeline_posts

# Wait for a few seconds to ensure the posts are retrieved
sleep 10

# Get the ID of the created post
echo "Obtaining ID of created post for deletion:"; post_id=$(curl -X GET "$BASE_URL/timeline_post" | jq -r '.timeline_posts[0].id')

# Wait for a few seconds to ensure the post is retrieved
sleep 10

# Delete the post
delete_timeline_post $post_id

# Wait for a few seconds to ensure the post is deleted
sleep 10

# Get all timeline posts again
get_timeline_posts

echo "Testing complete"