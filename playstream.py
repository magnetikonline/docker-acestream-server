#!/usr/bin/env python

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib2

DEFAULT_SERVER_HOSTNAME = '127.0.0.1'
DEFAULT_SERVER_PORT = 6878
SERVER_POLL_TIME = 2
SERVER_STATUS_STREAM_ACTIVE = 'dl'


def exit_error(message):
	sys.stderr.write('Error: {0}\n'.format(message))
	sys.exit(1)

def read_arguments():
	# create parser
	parser = argparse.ArgumentParser(
		description =
			'Instructs server to commence a given program ID. '
			'Will optionally execute a local media player once playback has started.'
	)

	parser.add_argument(
		'--ace-stream-pid',
		help = 'program ID to stream',
		metavar = 'HASH',
		required = True
	)

	parser.add_argument(
		'--player',
		help = 'media player to execute once stream active',
	)

	parser.add_argument(
		'--progress',
		action = 'store_true',
		help = 'continue to output stream statistics (connected peers/transfer rates) every {0} seconds'.format(SERVER_POLL_TIME)
	)

	parser.add_argument(
		'--server',
		default = DEFAULT_SERVER_HOSTNAME,
		help = 'server hostname, defaults to %(default)s',
		metavar = 'HOSTNAME'
	)

	parser.add_argument(
		'--port',
		default = DEFAULT_SERVER_PORT,
		help = 'server HTTP API port, defaults to %(default)s',
	)

	arg_list = parser.parse_args()

	if (not re.search(r'^[a-f0-9]{40}$',arg_list.ace_stream_pid)):
		exit_error('invalid stream program ID of [{0}] given'.format(arg_list.ace_stream_pid))

	# return arguments
	return (
		arg_list.ace_stream_pid,
		arg_list.player,
		arg_list.progress,
		arg_list.server,
		arg_list.port
	)

def api_request(uri):
	response = urllib2.urlopen(uri)
	return json.loads(response.read()).get('response',{})

def start_stream(server_hostname,server_port,stream_pid):
	# build stream UID from PID
	stream_uid = hashlib.sha1(stream_pid).hexdigest()

	# call API to commence stream
	response = api_request('http://{0}:{1}/ace/getstream?format=json&sid={2}&id={3}'.format(
		server_hostname,
		server_port,
		stream_uid,
		stream_pid
	))

	# return statistics API endpoint and HTTP video stream URLs
	return (
		response['stat_url'],
		response['playback_url']
	)

def stream_stats_message(response):
	return 'Peers: {0} // Down: {1}KB // Up: {2}KB'.format(
		response.get('peers',0),
		response.get('speed_down',0),
		response.get('speed_up',0)
	)

def await_playback(statistics_url):
	while (True):
		response = api_request(statistics_url)

		if (response.get('status') == SERVER_STATUS_STREAM_ACTIVE):
			# stream is ready
			print('Ready!\n')
			break

		else:
			print('Waiting... [{0}]'.format(stream_stats_message(response)))
			time.sleep(SERVER_POLL_TIME)

def execute_media_player(media_player_bin,playback_url):
	subprocess.Popen(
		media_player_bin.split() + [playback_url],
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE
	)

def stream_progress(statistics_url):
	print('')
	while (True):
		print('Streaming... [{0}]'.format(
			stream_stats_message(api_request(statistics_url))
		))

		time.sleep(SERVER_POLL_TIME)

def main():
	# read CLI arguments
	(
		stream_pid,
		media_player_bin,
		progress_follow,
		server_hostname,
		server_port
	) = read_arguments()

	print('Connecting to program ID [{0}]'.format(stream_pid))
	statistics_url,playback_url = start_stream(server_hostname,server_port,stream_pid)

	print('Awaiting successful playback of stream')
	await_playback(statistics_url)

	print('Playback started at [{0}]'.format(playback_url))
	if (media_player_bin is not None):
		print('Starting media player...')
		execute_media_player(media_player_bin,playback_url)

	if (progress_follow):
		stream_progress(statistics_url)

if (__name__ == '__main__'):
	main()
