#!/usr/bin/env python
import sys
import os
import signal
import subprocess
import argparse

import sockets

CAMERA_POSITIONS = ['front', 'rear', 'left', 'right']

class Handlers(sockets.StandardHandlers):
    def __init__(self, socket, position):
        super(Handlers, self).__init__(socket, 'camera', 'raspicam-' + position)
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
    sockets.listen_event_handlers(args.server, Handlers, args.position)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('position', type=str, choices=CAMERA_POSITIONS,
                        help='Position of camera.')
    sockets.add_server_arg(parser)
    main(parser.parse_args())

