#!/bin/bash -e

DIRNAME=$(dirname "$0")
DOCKER_IMAGE_NAME="magnetikonline/acestream"


docker build \
	--tag "$DOCKER_IMAGE_NAME" \
	"$DIRNAME"
