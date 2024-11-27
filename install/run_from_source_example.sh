#!/bin/bash

# Download the repo and enter it
git clone https://github.com/jonathanfox5/gogadget
cd gogadget

# Create the virtual environment and install packages
uv sync

# Run the tool
uv run gogadget

# Alternatively, you can enter the venv and then run the tool in any directory you like
source .venv/bin/activate
gogadget