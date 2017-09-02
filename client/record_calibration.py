#!/usr/bin/env python
import os
import argparse
import subprocess

import picamera
import recordings
import convert_recording

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

CAMERA_POSITIONS = ['left', 'front-left', 'front-right', 'right']
FRAMERATE = 5
DURATION = 30
RESOLUTION = (1280, 960)

def main(args):
    calibration_name = 'calibration_' + args.position
    h264_path = recordings.get_path(calibration_name + '.h264')
    with picamera.PiCamera() as camera:
        camera.resolution = RESOLUTION
        camera.vflip = True
        camera.hflip = True
        camera.framerate = FRAMERATE
        print('Recording to {}...'.format(h264_path))
        camera.start_recording(h264_path)
        camera.wait_recording(DURATION)
        camera.stop_recording()
    convert_recording.convert(calibration_name, input_framerate=FRAMERATE)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('position', type=str, choices=CAMERA_POSITIONS,
                        help='Position of camera.')
    main(parser.parse_args())

