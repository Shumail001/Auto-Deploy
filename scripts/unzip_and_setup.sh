#!/bin/bash
# Navigate to deployment directory
cd /home/ubuntu/

# Unzip the application
unzip -o app.zip -d app/

# Navigate to the app directory
cd app/

# Install dependencies
pip3 install -r requirements.txt
