#!/usr/bin/env python
import os
import argparse
import subprocess

import picamera
import recordings

def main(args):
    recording_name = os.path.splitext(os.path.basename(args.input_path))[0]
    convert(recording_name)

def convert(recording_name, input_framerate=15, output_framerate=15):
    h264_path = recordings.get_path(recording_name + '.h264')
    mjpeg_path = recordings.get_path(recording_name + '.avi')
    print('Converting to {}...'.format(mjpeg_path))
    subprocess.call(['avconv', '-r', str(input_framerate), '-i', h264_path,
                     '-c:v', 'mjpeg', '-q:v', '2', '-an', '-r', str(output_framerate), mjpeg_path])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str, help='Path of input h264 file.')
    main(parser.parse_args())

