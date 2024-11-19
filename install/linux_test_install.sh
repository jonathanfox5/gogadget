#!/bin/bash

# Update system and install binary requirements
sudo apt update -y && sudo apt install -y
sudo apt install ffmpeg build-essential python3-dev git

# Install uv and poetry
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv tool install poetry

# Build python package
git clone https://github.com/jonathanfox5/gogadget
cd gogadget
poetry build

# Find the wheel and install it
whl_file=$(ls dist/*.whl | head -n 1)

if [ -z "$whl_file" ]; then
    echo "No .whl file found in the dist directory."
    exit 1
fi

uv tool install "$whl_file" --python 3.10 --update

