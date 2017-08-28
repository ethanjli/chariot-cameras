#!/usr/bin/env python
import os
import argparse
import subprocess

import picamera

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

CAMERA_POSITIONS = ['front', 'rear', 'left', 'right']

def main(args):
    calibration_name = 'calibration_' + args.position
    h264_path = os.path.join(MODULE_PATH, calibration_name + '.h264')
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 960)
        camera.vflip = True
        camera.hflip = True
        camera.framerate = 5
        #print('Recording to {}...'.format(h264_path))
        #camera.start_recording(h264_path)
        #camera.wait_recording(30)
        #camera.stop_recording()
    mjpeg_path = os.path.join(MODULE_PATH, calibration_name + '.avi')
    print('Converting to {}...'.format(mjpeg_path))
    subprocess.call(['avconv', '-r', '15', '-i', h264_path,
                     '-c:v', 'mjpeg', '-q:v', '2', '-an', '-r', '15', mjpeg_path])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('position', type=str, choices=CAMERA_POSITIONS,
                        help='Position of camera.')
    main(parser.parse_args())

