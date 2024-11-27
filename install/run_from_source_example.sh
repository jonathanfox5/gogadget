#!/bin/bash

# Download the repo and enter it
git clone https://github.com/jonathanfox5/gogadget
cd gogadget

# Create the virtual environment and install packages
uv sync

# Enter the virtual environment
source .venv/bin/activate

# Run the tool
uv run gogadget

# Alternatively
source .venv/bin/activate
gogadget