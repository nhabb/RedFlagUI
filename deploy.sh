#!/bin/bash

# Deploy script for RedFlag SOC Dashboard
# This script commits and pushes changes to GitHub

# Navigate to the project directory
cd /home/hackme/hackathon_UI/RedFlagUI

# Add all changes to git
git add .

# Commit with a message (you can change the message as needed)
git commit -m "Update RedFlag SOC Dashboard"

# Push to GitHub
git push origin main

echo "✅ Successfully deployed to GitHub!"
echo "🚀 Your Streamlit Cloud deployment will update automatically"
