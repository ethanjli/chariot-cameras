#!/usr/bin/env python
import socketIO_client
import functools
import random
import time

#HOST = 'http://secret-fortress-28416.herokuapp.com'
HOST = 'localhost'
PORT = 80

def on_connect(socketIO):
    print('Connected')

def on_reconnect(socketIO):
    print('Reconnected')

def on_disconnect(socketIO):
    print('Disconnected')

def on_echo(socketIO, *args):
    print('echo', args[0])
    time.sleep(0.5)
    socketIO.emit('echo', random.randint(0, 100))

def register_event_handler(socketIO, handler_name, handler):
    socketIO.on(handler_name, functools.partial(handler, socketIO))

def main():
    with socketIO_client.SocketIO(HOST, PORT) as socketIO:
        register_event_handler(socketIO, 'connect', on_connect)
        register_event_handler(socketIO, 'disconnect', on_disconnect)
        register_event_handler(socketIO, 'reconnect', on_reconnect)
        register_event_handler(socketIO, 'echo', on_echo)
        socketIO.emit('echo', random.randint(0, 100))
        socketIO.wait()


if __name__ == '__main__':
    main()
