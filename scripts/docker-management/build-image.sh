#!/bin/bash
set -e

DIR=$(dirname "$(realpath "$0")")
cd "$DIR/../.."

IMAGE_NAME=$(cat "$DIR/../../NAME")
IMAGE_TAG=$(cat "$DIR/../../VERSION")

echo "Building image $IMAGE_NAME:$IMAGE_TAG"
docker build . -t "$IMAGE_NAME:$IMAGE_TAG"