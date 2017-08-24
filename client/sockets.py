from functools import partial

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

class Handlers(object):
    def __init__(self, socket):
        self.socket = socket

class StandardHandlers(Handlers):
    def __init__(self, socket, client, client_type):
        super(StandardHandlers, self).__init__(socket)
        self.client = client
        self.client_type = client_type

    def connect(self):
        print('[Sockets] Connected to server.')
        self.socket.emit('connected', {
            'client': self.client,
            'clientType': self.client_type
        })

    def disconnect(self):
        print('[Sockets] Disconnected from server.')

    def reconnect(self):
        print('[Sockets] Reconnected to server.')

def register_event_handler(socket, handler_name, handler):
    socket.on(handler_name, partial(handler, socket))

def register_event_handlers(socket, handlers_object):
    for handler_name in dir(handlers_object):
        if not handler_name.startswith('__') and not handler_name.endswith('__'):
            socket.on(handler_name, getattr(handlers_object, handler_name))

