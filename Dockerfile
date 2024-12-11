FROM debian:10-slim
LABEL maintainer="Peter Mescalchin <peter@magnetikonline.com>"

ARG ACE_STREAM_VERSION

# install packages
RUN DEBIAN_FRONTEND="noninteractive" \
	apt-get update && apt-get --yes upgrade && \
	apt-get --no-install-recommends --yes install \
		curl \
		ca-certificates \
		libpython2.7 \
		net-tools \
		python-apsw \
		python-lxml \
		python-m2crypto \
		python-pkg-resources \
		python-requests && \
	# clean up
	apt-get clean && \
	rm --force --recursive /var/lib/apt/lists
# install server
WORKDIR /acestream
RUN curl --silent "https://download.acestream.media/linux/acestream_${ACE_STREAM_VERSION}_x86_64.tar.gz" | \
                  tar --extract --gzip

EXPOSE 6878/tcp

ENTRYPOINT ["/acestream/start-engine"]
CMD ["--client-console"]
