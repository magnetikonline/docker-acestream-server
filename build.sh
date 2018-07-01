#!/bin/bash -e

DIRNAME=$(dirname "$0")
DOCKER_IMAGE_NAME="magnetikonline/acestream-server"


docker build \
	--tag "$DOCKER_IMAGE_NAME" \
	"$DIRNAME"
