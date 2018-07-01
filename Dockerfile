FROM debian:8
LABEL maintainer="Peter Mescalchin <peter@magnetikonline.com>"

ENV VERSION="3.1.16_debian_8.7"

RUN apt-get update && apt-get upgrade --yes && \
	apt-get install --yes curl libpython2.7 libxslt1.1 python-apsw python-m2crypto python-minimal python-setuptools && \
	apt-get clean && \
	curl --silent "http://dl.acestream.org/linux/acestream_${VERSION}_x86_64.tar.gz" | \
		tar --extract --gzip && \
	mv "acestream_${VERSION}_x86_64" /opt/acestream

EXPOSE 6878

CMD ["/opt/acestream/acestreamengine","--client-console"]
