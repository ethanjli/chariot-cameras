import os
import errno

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
REPOSITORY_PATH = os.path.dirname(MODULE_PATH)
RECORDINGS_PATH = os.path.join(os.path.dirname(REPOSITORY_PATH), 'recordings')

def make_dir_path(path):
    try:
        os.makedirs(path)
        os.chmod(path, 0777) # chmod a+rwx
    except OSError as e:
        if not (e.errno == errno.EEXIST and os.path.isdir(path)):
            raise

def get_path(recording_filename):
    return os.path.join(RECORDINGS_PATH, recording_filename)

