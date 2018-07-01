#!/bin/bash -e

DOCKER_IMAGE_NAME="magnetikonline/acestream-server"
SERVER_HTTP_PORT="6878"
STATE_DIR="/root/.ACEStream"
STATE_TMPFS_SIZE_MB="4096"


docker run \
	--publish "$SERVER_HTTP_PORT:$SERVER_HTTP_PORT" \
	--rm \
	--tmpfs "$STATE_DIR:noexec,rw,size=${STATE_TMPFS_SIZE_MB}m" \
		"$DOCKER_IMAGE_NAME"
