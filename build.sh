#!/bin/bash -e

DIRNAME=$(dirname "$0")
DOCKER_REPOSITORY=${DOCKER_REPOSITORY-"magnetikonline/acestream-server"}


. "$DIRNAME/version"

docker build \
	--build-arg "ACE_STREAM_VERSION=$ACE_STREAM_VERSION" \
	--tag "$DOCKER_REPOSITORY:$ACE_STREAM_VERSION" \
		"$DIRNAME"
