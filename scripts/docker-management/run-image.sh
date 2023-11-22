#!/bin/bash
set -e

DIR=$(dirname "$(realpath "$0")")
cd "$DIR/../.."

IMAGE_NAME=$(cat "$DIR/../../NAME")
IMAGE_TAG=$(cat "$DIR/../../VERSION")
PORT=$(cat "$DIR/../port.txt")
ORG_NAME="similar-intelligence"

if [ "$(lsof -i :$PORT)" ]; then
  echo "Port $PORT is in use. Shutting it down."

  # Get the container ID using the port
  CONTAINER_ID=$(docker ps -q --filter "publish=$PORT" --format "{{.ID}}")

  # Stop the container if the ID is not empty
  if [ -n "$CONTAINER_ID" ]; then
    docker container stop "$CONTAINER_ID"
  else
    echo "No container found using port $PORT."
  fi
fi

echo "Running image $IMAGE_NAME:$IMAGE_TAG"
docker run -p $PORT:$PORT -d -t ghcr.io/$ORG_NAME/$IMAGE_NAME:$IMAGE_TAG