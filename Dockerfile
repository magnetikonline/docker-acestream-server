FROM debian:8-slim
LABEL maintainer="Peter Mescalchin <peter@magnetikonline.com>"

ENV VERSION="3.1.16_debian_8.7"

RUN apt-get update && apt-get upgrade --yes && \
	apt-get install --no-install-recommends --yes \
		curl \
		libpython2.7 \
		net-tools \
		python-apsw \
		python-lxml \
		python-m2crypto \
		python-pkg-resources && \
	apt-get clean && \
	rm --force --recursive /var/lib/apt/lists && \
	curl --silent "http://dl.acestream.org/linux/acestream_${VERSION}_x86_64.tar.gz" | \
		tar --extract --gzip && \
	mv "acestream_${VERSION}_x86_64" /opt/acestream

EXPOSE 6878

CMD ["/opt/acestream/acestreamengine","--client-console"]
