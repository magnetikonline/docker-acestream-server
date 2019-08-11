FROM debian:8-slim
LABEL maintainer="Peter Mescalchin <peter@magnetikonline.com>"

ARG ACE_STREAM_VERSION

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
	curl --silent "http://dl.acestream.org/linux/acestream_${ACE_STREAM_VERSION}_x86_64.tar.gz" | \
		tar --extract --gzip && \
	mv "acestream_${ACE_STREAM_VERSION}_x86_64" /opt/acestream && \
	echo "/opt/acestream/lib" >>/etc/ld.so.conf && \
	/sbin/ldconfig

EXPOSE 6878

CMD ["/opt/acestream/acestreamengine","--client-console"]
