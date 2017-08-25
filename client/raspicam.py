#!/usr/bin/env python
import sys
import os
import signal
import subprocess
import argparse

import picamera

import sockets

CAMERA_POSITIONS = ['front', 'rear', 'left', 'right']

class Handlers(sockets.StandardHandlers):
    def __init__(self, socket, position, quit):
        super(Handlers, self).__init__(socket, 'camera', 'raspicam-' + position)
        self.camera = picamera.PiCamera()
        self.camera.vflip = True
        self.camera.hflip = True
        self.camera.resolution = (1280, 960)
        self.quit = quit

    def shutdown(self):
        print('[Recording] Shutting down...')
        self.camera.close()
        if self.quit:
            sys.exit()
        else:
            subprocess.call('sudo shutdown -h now', shell=True)

    def start(self):
        print('[Recording] Starting recording...')
        self.camera.start_recording('test.h264')

    def stop(self):
        print('[Recording] Stopping recording...')
        self.camera.stop_recording()

def main(args):
    sockets.listen_event_handlers(args.server, Handlers,
                                  args.position, args.quit)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('position', type=str, choices=CAMERA_POSITIONS,
                        help='Position of camera.')
    parser.add_argument('--quit', action="store_true", default=True,
                        help='Quit instead of shutting down the system.')
    sockets.add_server_arg(parser, default_server='tessel')
    main(parser.parse_args())

