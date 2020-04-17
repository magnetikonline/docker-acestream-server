#!/usr/bin/env python3

import argparse
import hashlib
import json
import re
import signal
import subprocess
import sys
import time
import urllib.request


DEFAULT_SERVER_HOSTNAME = "127.0.0.1"
DEFAULT_SERVER_PORT = 6878
SERVER_POLL_TIME = 2
SERVER_STATUS_STREAM_ACTIVE = "dl"


def exit_error(message):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


class WatchSigint:
    _sent = None

    def __init__(self):
        if WatchSigint._sent is None:
            # install handler
            WatchSigint._sent = False
            signal.signal(signal.SIGINT, self._handler)

    def _handler(self, signal, frame):
        # Ctrl-C (SIGINT) sent to process
        WatchSigint._sent = True

    def sent(self):
        return WatchSigint._sent


def read_arguments():
    # create parser
    parser = argparse.ArgumentParser(
        description="Instructs server to commence a given program ID. "
        "Will optionally execute a local media player once playback has started."
    )

    parser.add_argument(
        "--ace-stream-pid", help="program ID to stream", metavar="HASH", required=True
    )

    parser.add_argument("--player", help="media player to execute once stream active")

    parser.add_argument(
        "--progress",
        action="store_true",
        help=f"continue to output stream statistics (connected peers/transfer rates) every {SERVER_POLL_TIME} seconds",
    )

    parser.add_argument(
        "--server",
        default=DEFAULT_SERVER_HOSTNAME,
        help="server hostname, defaults to %(default)s",
        metavar="HOSTNAME",
    )

    parser.add_argument(
        "--port",
        default=DEFAULT_SERVER_PORT,
        help="server HTTP API port, defaults to %(default)s",
    )

    arg_list = parser.parse_args()

    if not re.search(r"^[a-f0-9]{40}$", arg_list.ace_stream_pid):
        exit_error(f"invalid stream program ID of [{arg_list.ace_stream_pid}] given")

    # return arguments
    return (
        arg_list.ace_stream_pid,
        arg_list.player,
        arg_list.progress,
        arg_list.server,
        arg_list.port,
    )


def api_request(url):
    response = urllib.request.urlopen(url)
    return json.load(response).get("response", {})


def start_stream(server_hostname, server_port, stream_pid):
    # build stream UID from PID
    stream_uid = hashlib.sha1(stream_pid.encode()).hexdigest()

    # call API to commence stream
    response = api_request(
        f"http://{server_hostname}:{server_port}/ace/getstream?format=json&sid={stream_uid}&id={stream_pid}"
    )

    # return statistics API endpoint and HTTP video stream URLs
    return (response["stat_url"], response["playback_url"])


def stream_stats_message(response):
    return (
        f'Peers: {response.get("peers", 0)} // '
        f'Down: {response.get("speed_down", 0)}KB // '
        f'Up: {response.get("speed_up", 0)}KB'
    )


def await_playback(watch_sigint, statistics_url):
    while True:
        response = api_request(statistics_url)

        if response.get("status") == SERVER_STATUS_STREAM_ACTIVE:
            # stream is ready
            print("Ready!\n")
            return True

        if watch_sigint.sent():
            # user sent SIGINT, exit now
            print("\nExit!")
            return False

        # pause and check again
        print(f"Waiting... [{stream_stats_message(response)}]")
        time.sleep(SERVER_POLL_TIME)


def execute_media_player(media_player_bin, playback_url):
    subprocess.Popen(
        media_player_bin.split() + [playback_url],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def stream_progress(watch_sigint, statistics_url):
    print("")
    while True:
        print(f"Streaming... [{stream_stats_message(api_request(statistics_url))}]")

        if watch_sigint.sent():
            # user sent SIGINT, exit now
            print("\nExit!")
            return

        time.sleep(SERVER_POLL_TIME)


def main():
    # read CLI arguments
    (
        stream_pid,
        media_player_bin,
        progress_follow,
        server_hostname,
        server_port,
    ) = read_arguments()

    # create Ctrl-C watcher
    watch_sigint = WatchSigint()

    print(f"Connecting to program ID [{stream_pid}]")
    statistics_url, playback_url = start_stream(
        server_hostname, server_port, stream_pid
    )

    print("Awaiting successful connection to stream")
    if not await_playback(watch_sigint, statistics_url):
        # exit early
        return

    print(f"Playback available at [{playback_url}]")
    if media_player_bin is not None:
        print("Starting media player...")
        execute_media_player(media_player_bin, playback_url)

    if progress_follow:
        stream_progress(watch_sigint, statistics_url)


if __name__ == "__main__":
    main()
