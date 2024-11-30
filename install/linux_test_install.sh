#!/bin/bash

# Update system and install binary requirements
sudo apt update -y && sudo apt install -y
sudo apt install ffmpeg build-essential python3-dev git tree -y

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Build python package
git clone https://github.com/jonathanfox5/gogadget
uv build gogadget

# Find the wheel and install it
whl_file=$(ls gogadget/dist/*.whl | head -n 1)

if [ -z "$whl_file" ]; then
    echo "No .whl file found in the dist directory."
    exit 1
fi

# Python 3.10 is used due to certain dependencies having 
# compatibility issues with linux ARM on newer versions
uv tool install "$whl_file" --python 3.10
