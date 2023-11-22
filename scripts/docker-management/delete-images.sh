#!/bin/bash
set -e

DIR=$(dirname "$(realpath "$0")")
cd "$DIR"

# delete images without a tag
docker rmi -f $(docker images -f "dangling=true" -q)