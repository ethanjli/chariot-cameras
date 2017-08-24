#!/usr/bin/env python
import sys
import os
import signal
import subprocess
import argparse

import socketIO_client

import sockets

# SOCKET.IO HANDLERS

class Handlers(sockets.StandardHandlers):
    def __init__(self, socket):
        super(Handlers, self).__init__(socket, 'camera', 'test-client')
        self.process = None

    def shutdown(self):
        print('[Recording] Shutting down...')
        sys.exit()

    def start(self):
        print('[Recording] Starting recording...')
        self.process = subprocess.Popen(['yes'])
        print('[Recording] Started recording.')

    def stop(self):
        print('[Recording] Stopping recording...')
        os.kill(self.process.pid, signal.SIGINT)
        self.process.wait()
        print('[Recording] Stopped recording.')

def main(args):
    server = sockets.SERVERS[args.server]
    with socketIO_client.SocketIO(server['host'], server['port']) as socket:
        sockets.register_event_handlers(socket, Handlers(socket))
        socket.wait()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', type=str, choices=sockets.SERVERS.keys(),
                        help='Server to connect to.', default='local')
    args = parser.parse_args()
    main(args)

