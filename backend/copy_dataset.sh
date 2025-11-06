#!/bin/bash
# Script to copy dataset for Railway/Nixpacks deployment

# Try to find and copy the dataset
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

DATASET_SOURCE="$PROJECT_ROOT/src/assets/resume-dataset.csv"
DATASET_DEST="$SCRIPT_DIR/resume-dataset.csv"

if [ -f "$DATASET_SOURCE" ]; then
    cp "$DATASET_SOURCE" "$DATASET_DEST"
    echo "Dataset copied successfully to backend directory"
else
    echo "WARNING: Dataset not found at $DATASET_SOURCE"
    echo "ML model will use heuristic fallback"
fi

