#!/bin/bash -e

DOCKER_IMAGE_NAME="magnetikonline/acestream-server"
SERVER_HTTP_PORT="6878"


docker run \
	--publish "$SERVER_HTTP_PORT:$SERVER_HTTP_PORT" \
	--rm \
	--tmpfs "/dev/disk/by-id:noexec,rw,size=4k" \
		"$DOCKER_IMAGE_NAME"
