#!/bin/bash

# Create the directory for weights if it doesn't exist
mkdir -p weights

# Download the file
wget -q https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -P weights


