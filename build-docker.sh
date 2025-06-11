#!/bin/bash
set -e

IMAGE_NAME="meetily-backend"

docker build -t $IMAGE_NAME -f backend/Dockerfile .

echo "Image built: $IMAGE_NAME"

docker run --rm -p 5167:5167 -p 8178:8178 $IMAGE_NAME

