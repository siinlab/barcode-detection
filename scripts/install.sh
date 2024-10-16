#!/bin/bash
set -e

DIR=$(dirname "$(realpath "$0")")
cd "$DIR"

export DEBIAN_FRONTEND=noninteractive

apt-get update -y || true
apt-get install ffmpeg libsm6 libxext6  -y || true

cd "$DIR/.."
export TMPDIR=$HOME/tmp
pip --cache-dir /home/tmp install -r requirements.txt 