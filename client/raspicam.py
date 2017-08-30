#!/usr/bin/env python
import sys
import os
import signal
import subprocess
import time
import datetime
import argparse

import netifaces as ni
import picamera

import sockets
import recordings

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

CAMERA_POSITIONS = ['front', 'rear', 'left', 'right']

def time_to_ms(unix_timestamp):
    return int(round(unix_timestamp * 1000))

def time_to_structure(unix_timestamp):
    dt = datetime.datetime.fromtimestamp(unix_timestamp)
    return {
        'iso': dt.isoformat() + 'Z',
        'unix': time_to_ms(unix_timestamp)
    }

class Handlers(sockets.StandardHandlers):
    def __init__(self, socket, position, quit):
        super(Handlers, self).__init__(socket, 'camera', 'raspicam-' + position)
        self.position = position
        self.quit = quit
        
        self.camera = picamera.PiCamera()
        self.camera.vflip = True
        self.camera.hflip = True
        self.camera.resolution = (1280, 960)
        self.camera.framerate = 15

        self.recording = False
        self.recording_name = None

        self.ip = None
    
    def connect(self):
        print('[Sockets] Connected to server.')
        self.ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
        self.socket.emit('connected', {
            'client': self.client,
            'clientType': self.client_type,
            'metadata': {
                'ip': self.ip
            }
        })

    def shutdown(self):
        print('[Recording] Shutting down...')
        self.camera.close()
        if self.quit:
            sys.exit()
        else:
            subprocess.call('sudo shutdown -h now', shell=True)

    def start(self):
        print('[Recording] Starting recording...')
        current_time = time.time()
        self.recording_name = '{}_{}.h264'.format(self.position, time_to_ms(current_time))
        self.socket.emit('event', {
            'name': 'cameraRecordingStarted',
            'position': self.position,
            'cameraTime': time_to_structure(current_time),
            'recordingName': self.recording_name
        })
        recordings.make_dir_path(recordings.RECORDINGS_PATH)
        self.camera.start_recording(os.path.join(MODULE_PATH, recordings.get_path(self.recording_name)))
        self.recording = True

    def stop(self):
        print('[Recording] Stopping recording...')
        current_time = time.time()
        if self.recording:
            self.camera.stop_recording()
            os.chmod(recordings.get_path(self.recording_name), 0666) # chmod a+rw
            self.socket.emit('event', {
                'name': 'cameraRecordingStopped',
                'position': self.position,
                'cameraTime': time_to_structure(current_time),
                'recordingName': self.recording_name
            })
            self.recording_name = None
        else:
            self.socket.emit('event', {
                'name': 'cameraRecordingError',
                'position': self.position,
                'error': 'Server requested camera to stop recording, but camera was not recording.',
                'cameraTime': time_to_structure(current_time)
            })

def main(args):
    sockets.listen_event_handlers(args.server, Handlers,
                                  args.position, args.quit)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('position', type=str, choices=CAMERA_POSITIONS,
                        help='Position of camera.')
    parser.add_argument('--quit', action="store_true", default=False,
                        help='Quit instead of shutting down the system.')
    sockets.add_server_arg(parser, default_server='tessel')
    main(parser.parse_args())

