#!/bin/bash -e

DOCKER_IMAGE_NAME="magnetikonline/acestream-server"
SERVER_HTTP_PORT="6878"


docker run \
	--publish "$SERVER_HTTP_PORT:$SERVER_HTTP_PORT" \
	--rm \
		"$DOCKER_IMAGE_NAME"
