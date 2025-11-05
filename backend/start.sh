#!/bin/bash
set -e

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Print environment info
echo "=== Environment Info ==="
echo "Working Directory: $(pwd)"
echo "PORT: ${PORT:-not set}"
echo "Python: $(which python3)"
echo "Python Version: $(python3 --version)"
echo "========================="

# Start the server
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

