#!/usr/bin/env python
import os
import argparse

import picamera
import recordings
import convert_recording

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

CAMERA_POSITIONS = ['left', 'front-left', 'front-right', 'right']
FRAMERATE = 2
DURATION = 120
RESOLUTION = (1280, 960)

def main(args):
    calibration_name = 'calibration_' + args.position
    h264_path = recordings.get_path(calibration_name + '.h264')
    with picamera.PiCamera() as camera:
        camera.resolution = RESOLUTION
        camera.framerate = FRAMERATE
        camera.exposure_mode = 'sports'
        camera.awb_mode = 'off'
        camera.awb_gains = (1.25, 1.5)
        print('Recording to {}...'.format(h264_path))
        camera.start_preview()
        camera.preview.alpha = 128
        camera.start_recording(h264_path, level='4.2', bitrate=30000000, quality=20)
        for i in range(DURATION):
            print(i)
            camera.wait_recording(1)
        camera.stop_recording()
        camera.stop_preview()
    convert_recording.convert(calibration_name, input_framerate=FRAMERATE, output_framerate=FRAMERATE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('position', type=str, choices=CAMERA_POSITIONS,
                        help='Position of camera.')
    main(parser.parse_args())

