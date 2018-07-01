# Docker Ace Stream server
An [Ace Stream](http://www.acestream.org/) server running as a Docker container.
- [Overview](#overview)
- [Building](#building)
- [Usage](#usage)
- [Reference](#reference)

## Overview
What this provides:
- A Dockerized Ace Stream server (version `3.1.16`) on Debian 8 (Jessie).
- Bash script to start server and publish it's HTTP API endpoint to host system.
- Python playback script [`playstream.py`](playstream.py) instructing server to:
	- Commence streaming of a given Ace Stream program ID.
	- ...and (optionally) once ready start a compatible media player (e.g. [VLC](https://www.videolan.org/vlc/)) to playback the presented video stream over HTTP.

Since the Docker Ace Stream server is both controlled by, and provides a usable video stream over a single HTTP endpoint/port this should offer one of the easier methods to get Ace Stream running on unsupported operating systems such as OS X.

## Building
To build Docker image:
```sh
$ ./build.sh
```

Alternatively pull the pre-built image from Docker Hub:
```sh
$ docker pull magnetikonline/acestream-server
```

## Usage
Start the Ace Stream server via:
```sh
$ ./run.sh
```

If using a Linux host the alternative [`run-tmpfs.sh`](run-tmpfs.sh) is recommended which mounts the server cache directory into a [temporary based `tmpfs`](run-tmpfs.sh#L12) filesystem inside the running Docker container. This saves thrashing out the stream contents to disk, which the server seems to do without control.

The server will now be running with a HTTP API endpoint available at `http://127.0.0.1:6878/`:

```sh
$ curl http://127.0.0.1:6878/webui/api/service?method=get_version
# {"result": {"code": 3011600, "platform": "linux", "version": "3.1.16"}, "error": null}
```

A program ID can now be started with [`playstream.py`](playstream.py):
```sh
$ ./playstream.py --help
usage: playstream.py [-h] --ace-stream-pid HASH [--player PLAYER] [--progress]
                     [--server HOSTNAME] [--port PORT]

Instructs server to commence a given program ID. Will optionally execute a
local media player once playback has started.

optional arguments:
  -h, --help            show this help message and exit
  --ace-stream-pid HASH
                        program ID to stream
  --player PLAYER       media player to execute once stream active
  --progress            continue to output stream statistics (connected
                        peers/transfer rates) every 2 seconds
  --server HOSTNAME     server hostname, defaults to 127.0.0.1
  --port PORT           server HTTP API port, defaults to 6878
```

To start streaming a program ID of `PROGRAM_ID` and send playback to `vlc` when ready:
```sh
$ ./playstream.py \
	--ace-stream-pid PROGRAM_ID \
	--player vlc \
	--progress
```

## Reference
- [Ace Stream Wiki (English)](http://wiki.acestream.org/wiki/index.php/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0/en).
- Binary downloads: http://wiki.acestream.org/wiki/index.php/Download.
- Ubuntu install notes: http://wiki.acestream.org/wiki/index.php/Install_Ubuntu.
- HTTP API usage: http://wiki.acestream.org/wiki/index.php/Engine_HTTP_API.
- `playstream.py` routines inspired by: https://github.com/jonian/acestream-launcher.
