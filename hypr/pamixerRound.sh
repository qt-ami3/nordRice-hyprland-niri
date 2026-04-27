#!/bin/bash

current=$(pamixer --get-volume) # Get current volume (integer)

rounded=$(( (current + 2) / 5 * 5 )) # Round to nearest multiple of 5

pamixer --allow-boost --set-volume "$rounded"  # Set the rounded volume

echo "Volume rounded: $current → $rounded" #print function for testing
