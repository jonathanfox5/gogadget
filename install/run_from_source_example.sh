#!/bin/bash

# Download the repo and enter it
git clone https://github.com/jonathanfox5/gogadget
cd gogadget

# Create the virtual environment and install packages
poetry install

# Enter the virtual environment
poetry shell

# Run the tool
gogadget
