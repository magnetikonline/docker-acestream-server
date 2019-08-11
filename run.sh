#!/bin/bash -e

DIRNAME=$(dirname "$0")
DOCKER_REPOSITORY="magnetikonline/acestream-server"
SERVER_HTTP_PORT="6878"


. "$DIRNAME/version"

docker run \
	--publish "$SERVER_HTTP_PORT:$SERVER_HTTP_PORT" \
	--rm \
	--tmpfs "/dev/disk/by-id:noexec,rw,size=4k" \
		"$DOCKER_REPOSITORY:$ACE_STREAM_VERSION"
