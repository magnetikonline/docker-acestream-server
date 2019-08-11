#!/bin/bash -e

DIRNAME=$(dirname "$0")
DOCKER_REPOSITORY="magnetikonline/acestream-server"
SERVER_HTTP_PORT="6878"
STATE_DIR="/root/.ACEStream"
STATE_TMPFS_SIZE_MB="4096"


. "$DIRNAME/version"

docker run \
	--publish "$SERVER_HTTP_PORT:$SERVER_HTTP_PORT" \
	--rm \
	--tmpfs "/dev/disk/by-id:noexec,rw,size=4k" \
	--tmpfs "$STATE_DIR:noexec,rw,size=${STATE_TMPFS_SIZE_MB}m" \
		"$DOCKER_REPOSITORY:$ACE_STREAM_VERSION"
