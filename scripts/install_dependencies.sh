#!/bin/bash
# Update package index
sudo apt-get update -y

# Install Python and pip
sudo apt-get install -y python3 python3-pip unzip

# Ensure awscli is installed
sudo pip3 install awscli
