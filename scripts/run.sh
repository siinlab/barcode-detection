#!/bin/bash
set -e

DIR=$(dirname "$(realpath "$0")")
cd "$DIR"

export DEBIAN_FRONTEND=noninteractive

APP_PORT=$(cat $DIR/port.txt)

# Run the app
cd "$DIR/../src"
uvicorn main:app --host localhost --port  $APP_PORT