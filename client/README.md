# chariot-cameras clients
This contains various Python clients to connect to the `chariot-cameras` server.

## Test Client
This is a test client useful for testing connections to the server. Run `python test-client.py --server local` to connect to a local server, or substitute `local` with `heroku` or `tessel` to connect to the servers deployed on Heroku or Tessel, respectively.

## Raspberry Pi Camera Client
This is an actual client intended for headless deployment on a Raspberry Pi board with a wi-fi connection to a Tessel board running the `chariot-cameras` server as a wireless access point. Run `python raspicam.py left` to run the client as the controller for the left camera, or substitute `left` with `front-left`, `front-right`, or `right` to run the client as a controller for the those respective cameras. To connect to the Heroku server, add `--server heroku`. To make shutdown simply quit the program rather than halting the entire computer, add `--quit`.

## Raspberry Pi Deployment Setup
These instructions are for deployment on the Raspberry Pi Zero W.
* Download the [Raspbian Stretch](https://www.raspberrypi.org/downloads/raspbian/) image.
* Write it to the micro SD card using Etcher, following [these instructions](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).
* Change the password using `passwd`.
* You can uninstall useless programs: `sudo apt-get purge wolfram-engine libreoffice* minecraft-pi sonic-pi; sudo apt-get clean; sudo apt-get autoremove`.
* Connect to the Stanford Visitor network.
* Install all updates with `sudo apt-get update; sudo apt-get upgrade`.
* Open the terminal. In the home directory, clone this repo as `git clone https://github.com/ethanjli/chariot-cameras.git`.
* Install the `socketIO-client` module as `sudo pip install socketIO-client`.
* Install `python-netifaces`.
* Install `libav-tools`. This is needed for the `record_calibration` script to convert a raw h264 recording to a MJPEG video for calibration.
* Add `export LC_ALL=C` to `.bashrc`.
* Run `sudo raspi-config`. Set the Hostname to be `chariot-left` (substitute `left` with the side the camera is on), and set the Boot to be "To CLI". In the "Interfaces" tab, enable the Camera and SSH. In Localisation options, set the locale to be `en_US` (with default locale `en_US.UTF-8`), the Timezone to be `America/Los Angeles`, the keyboard to `Generic 104-key PC` with the `English (US)` layout, and the Wi-fi Country to be "US".
* Open `wpa-supplicant.conf`: `sudo vim.tiny /etc/wpa_supplicant/wpa_supplicant.conf`. Add a network entry with priority 100 for the `chariot` network, so that the Raspberry Pi preferentially auto-connects to that network when the Tessel 2 server is active:
```
network={
    ssid="chariot"
    key_mgmt=NONE
    priority=100
    id_str="chariot"
}
```
* Copy `start-raspicam` into `/etc/network/if-up.d`. Copy `stop-raspicam` into `/etc/network/if-down.d`. Change the `SIDE` variable in `/etc/network/if-up.d` to be either `left`, `front-left`, `front-right`, or `right`, to indicate the camera.
* Deploy the synchronization server on the Tessel 2 board. The Raspberry Pi should automatically connect to the `chariot` wireless network created by the Tessel 2 server, and the client should automatically start. On the control panel, the board should show up as a connected client. Recordings from the camera will be saved to `~/recordings`, named according to the side the camera is on and the Unix timestamp in the camera's local time.

## Camera Calibration
* Run `python record_calibration.py left` (or with the other camera) to record a 30-second calibration video named `calibration_left.avi` (or correspondingly named for the other camera) in `~/recordings/calibration_left.avi`.
* Download gdrive from the `gdrive-linux-rpi` binary listed at [prasmussen/gdrive](https://github.com/prasmussen/gdrive) to the Downloads directory. `chmod a+x` it and move it to the home directory and rename it to `gdrive`. In the home directory, run `./gdrive about` and follow the authentication instructions.
* Upload the calibration video to Google Drive: in the home directory, run `./gdrive upload recordings/calibration_left.avi`. Download it on another computer and, on that computer, run [video2calibration](https://github.com/smidm/video2calibration): `python calibrate.py -fs 1 calibration_left.avi calibration_left.yml`; save the calibration results.

## Headless File Access
* ssh into the Raspberry Pi at the IP address listed on the control panel, using the username `pi`.
* In `~/chariot-cameras/client`, run `python convert_recording.py <path_of_h264_recording_to_convert>` to convert the `.h264` recording to a `.avi` MJPEG recording, for example `python convert_recording.py ~/recordings/left_1504085446107.h264`.
* Exit ssh. scp the `.avi` recording to the local computer, for example `scp pi@192.168.1.241:/home/pi/recordings/left_1504085446107.avi ./`

## Movie Undistortion
* In the local computer with the `video2calibration` repository used during camera calibration, open the `.avi` recording in ImageJ/Fiji through "Import"/"AVI...", using the default settings. Save it as an Image Sequence with JPEG format and an empty name.
* In the `video2calibration` repository, run the undistort script on the image sequence with the obtained camera calibration. For example, `python undistort.py /run/media/lietk12/6434-6531/calibration/Arducam/calibration_left.yml "/run/media/lietk12/6434-6531/data/Arducam_x1_0/*.jpg" /run/media/lietk12/6434-6531/data/Arducam_x1_0/undistorted/`. Note that the output directory must be created before running the undistort script.

