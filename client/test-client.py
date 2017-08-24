#!/usr/bin/env python
import sys
import functools
import random
import time
import argparse

import socketIO_client

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

def on_connect(socket):
    print('[Sockets] Connected to server.')
    socket.emit('connected', {'client': 'camera', 'clientType': 'test-client'})

def on_disconnect(socket):
    print('[Sockets] Disconnected from server.')

def on_reconnect(socket):
    print('[Sockets] Reconnected to server.')

def on_echo(socket, *args):
    print('[Sockets] Echo from server:', args[0])
    time.sleep(0.5)
    print('[Sockets] Echoing server:', args[0])
    socket.emit('echo', random.randint(0, 100))

def on_shutdown(socket):
    print('[Recording] Shutting down...')
    sys.exit()

def register_event_handler(socket, handler_name, handler):
    socket.on(handler_name, functools.partial(handler, socket))

def main(args):
    server = SERVERS[args.server]
    with socketIO_client.SocketIO(server['host'], server['port']) as socket:
        register_event_handler(socket, 'connect', on_connect)
        register_event_handler(socket, 'disconnect', on_disconnect)
        register_event_handler(socket, 'reconnect', on_reconnect)
        register_event_handler(socket, 'echo', on_echo)
        register_event_handler(socket, 'shutdown', on_shutdown)
        socket.emit('echo', random.randint(0, 100))
        socket.wait()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', type=str, choices=SERVERS.keys(),
                        help='Server to connect to.', default='local')
    args = parser.parse_args()
    main(args)
