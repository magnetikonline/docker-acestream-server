# Docker Ace Stream server
An [Ace Stream](http://www.acestream.org/) server Docker image.
- [Overview](#overview)
- [Building](#building)
- [Usage](#usage)
- [Reference](#reference)

## Overview
What this provides:
- Dockerized Ace Stream server (version `3.1.16`) running under Debian 8 (Jessie) slim.
- Bash script to start server and present HTTP API endpoint to host.
- Python playback script [`playstream.py`](playstream.py) instructing server to:
	- Commence streaming of a given program ID.
	- ...and (optionally) start a compatible media player (such as [VLC](https://www.videolan.org/vlc/)) once ready.

Since server is both controlled by and provides a video stream via a single HTTP endpoint, this provides one of the easier methods to playback Ace Streams on unsupported operating systems such as OS X.

## Building
This requires Python with version 2.7. You can check your current Python by typing:
```sh
$ python --version
>> Python 2.7.14
```
Should higher version be installed, use [virtualenv](https://virtualenv.pypa.io/en/stable/) or [conda](https://docs.anaconda.com/anaconda/install/) to install an environment with correct Python version.

To build Docker image:
```sh
$ ./build.sh
```

Alternatively pull the Docker Hub image:
```sh
$ docker pull magnetikonline/acestream-server
```

## Usage
Start the server via:
```sh
$ ./run.sh
```

For Linux hosts the alternative [`run-tmpfs.sh`](run-tmpfs.sh) is recommended, mounting the cache directory into a [temporary based `tmpfs`](run-tmpfs.sh#L12) file system. This saves thrashing of the file system as stream contents is written to disk - which does not seem possible to disable via server launch arguments.

Server should now be running with the API endpoint available at `http://127.0.0.1:6878/`:

```sh
$ curl http://127.0.0.1:6878/webui/api/service?method=get_version
# {"result": {"code": 3011600, "platform": "linux", "version": "3.1.16"}, "error": null}
```

A program ID can be started with [`playstream.py`](playstream.py):
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
	--player /usr/bin/vlc \
	--progress
```

Send <kbd>Ctrl + C</kbd> to exit.

## Troubleshooting
### ModuleNotFoundError: No module named 'urllib2'
```$ ./playstream.py --help
Traceback (most recent call last):
  File "./playstream.py", line 11, in <module>
    import urllib2
ModuleNotFoundError: No module named 'urllib2'
```
This means you tried to use Python 3 instead of Python 2.7. Please make sure to use Python 2.7 when running these scripts.

## Reference
- [Ace Stream Wiki (English)](http://wiki.acestream.org/wiki/index.php/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0/en).
- Binary downloads: http://wiki.acestream.org/wiki/index.php/Download.
- Ubuntu install notes: http://wiki.acestream.org/wiki/index.php/Install_Ubuntu.
- HTTP API usage: http://wiki.acestream.org/wiki/index.php/Engine_HTTP_API.
- `playstream.py` routines inspired by: https://github.com/jonian/acestream-launcher.
