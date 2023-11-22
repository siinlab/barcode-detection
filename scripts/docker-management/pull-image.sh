#!/bin/bash
set -e

DIR=$(dirname "$(realpath "$0")")
cd "$DIR/../.."

IMAGE_NAME=$(cat "$DIR/../../NAME")
IMAGE_TAG=$(cat "$DIR/../../VERSION")
PORT=$(cat "$DIR/../port.txt")
ORG_NAME="similar-intelligence"

docker login --username reda-bouzad --password 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 ghcr.io
docker pull ghcr.io/similar-intelligence/$IMAGE_NAME:$IMAGE_TAG