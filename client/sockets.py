from functools import partial

class Handlers(object):
    def __init__(self, socket):
        self.socket = socket

# STANDARD SOCKET.IO EVENT HANDLERS

def on_connect(socket, client, client_type):
    print('[Sockets] Connected to server.')
    socket.emit('connected', {'client': client, 'clientType': client_type})

def on_disconnect(socket):
    print('[Sockets] Disconnected from server.')

def on_reconnect(socket):
    print('[Sockets] Reconnected to server.')


def register_event_handler(socket, handler_name, handler):
    socket.on(handler_name, partial(handler, socket))

def register_standard_event_handlers(socket, client, client_type):
    register_event_handler(socket, 'connect', partial(
        on_connect, client=client, client_type=client_type
    ))
    register_event_handler(socket, 'disconnect', on_disconnect)
    register_event_handler(socket, 'reconnect', on_reconnect)

def register_event_handlers(socket, handlers_object):
    for handler_name in dir(handlers_object):
        if not handler_name.startswith('__') and not handler_name.endswith('__'):
            socket.on(handler_name, getattr(handlers_object, handler_name))

