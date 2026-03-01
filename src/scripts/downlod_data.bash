#!/usr/bin/env bash

# This script is responsible for downloading the ESA Anomaly Dataset and saving it in the appropriate directory.

# Parameters:
# -o/--output_path: The directory where the dataset will be saved.

# ESA Anomaly Dataset
# Published April 17, 2025 | Version v2
# https://zenodo.org/records/15237121
ESA_DATASET_URL="https://zenodo.org/api/records/15237121/files-archive"

# Check if the output path is set
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -o|--output_path) OUTPUT_PATH="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done
if [ -z "$OUTPUT_PATH" ]; then
    echo "Error: Output path is not set. Use -o or --output_path to specify the directory."
    exit 1
fi

# Check if OUTPUT_PATH is a valid path:
## Writeable folder
## Empty folder
## Create the folder if it doesn't exist
if [ -d "$OUTPUT_PATH" ]; then
    if [ ! -w "$OUTPUT_PATH" ]; then
        echo "Error: Output path is not writable."
        exit 1
    fi
    if [ "$(ls -A "$OUTPUT_PATH")" ]; then
        echo "Error: Output path is not empty."
        exit 1
    fi
else
    mkdir -p "$OUTPUT_PATH"
fi

# Download the dataset with progress bar and save it to the output path
echo "Downloading ESA Anomaly Dataset..."
wget --show-progress -O "$OUTPUT_PATH/esa_anomaly_dataset.zip" "$ESA_DATASET_URL"

# Unzip the downloaded file
echo "Unzipping the dataset..."
unzip -o "$OUTPUT_PATH/esa_anomaly_dataset.zip" -d "$OUTPUT_PATH"

# Remove the zip file after extraction
rm "$OUTPUT_PATH/esa_anomaly_dataset.zip"