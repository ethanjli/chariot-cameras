#!/usr/bin/env python
import sys
import os
import signal
import subprocess
import random
import time
import argparse

import socketIO_client

import sockets

SERVERS = {
    'local': {
        'host': 'localhost',
        'port': 80
    },
    'heroku': {
        'host': 'http://secret-fortress-28416.herokuapp.com',
        'port': 80
    },
    'tessel': {
        'host': None,
        'port': None
    }
}

# SOCKET.IO HANDLERS

class Handlers(sockets.Handlers):
    def __init__(self, socket):
        super(Handlers, self).__init__(socket)
        self.process = None

    def echo(self, *args):
        print('[Sockets] Echo from server:', args[0])
        time.sleep(0.5)
        print('[Sockets] Echoing server:', args[0])
        self.socket.emit('echo', random.randint(0, 100))

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
    server = SERVERS[args.server]
    with socketIO_client.SocketIO(server['host'], server['port']) as socket:
        sockets.register_standard_event_handlers(socket, 'camera', 'test-client')
        sockets.register_event_handlers(socket, Handlers(socket))
        socket.wait()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', type=str, choices=SERVERS.keys(),
                        help='Server to connect to.', default='local')
    args = parser.parse_args()
    main(args)
