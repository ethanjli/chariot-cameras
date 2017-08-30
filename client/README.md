# chariot-cameras clients
This contains various Python clients to connect to the `chariot-cameras` server.

## Test Client
This is a test client useful for testing connections to the server. Run `python test-client.py --server local` to connect to a local server, or substitute `local` with `heroku` or `tessel` to connect to the servers deployed on Heroku or Tessel, respectively.

## Raspberry Pi Camera Client
This is an actual client intended for headless deployment on a Raspberry Pi board with a wi-fi connection to a Tessel board running the `chariot-cameras` server as a wireless access point. Run `python raspicam.py front` to run the client as the controller for the front camera, or substitute `front` with `left`, `right`, or `rear` to run the client as a controller for the left, right, or rear cameras, respectively. To connect to the Heroku server, add `--server heroku`. To make shutdown simply quit the program rather than halting the entire computer, add `--quit`.

## Raspberry Pi Deployment Setup
Assuming the Raspberry Pi board is a Raspberry Pi Zero W running a preloaded NOOBS:
* Let NOOBS install Raspbian on the SD card.
* Change the password using `passwd`.
* Install all updates with `sudo apt-get update` and `sudo apt-get upgrade`.
* Add `export LC_ALL=C` to `.bashrc`.
* Run the "Raspberry Pi Configuration" graphical program. In the "System" tab, set the Hostname to be `chariot-front` (substitute `front` with the side the camera is on), and set the Boot to be "To CLI". In the "Interfaces" tab, enable the Camera and SSH. In the "Localisation" tab, set the locale to be "US", the keyboard to the "English (US)" layout, and the Wi-fi Country to be "US".
* Open the terminal. In the home directory, clone this repo as `git clone https://github.com/ethanjli/chariot-cameras.git`.
* Install the `socketIO-client` module as `sudo pip install socketIO-client`.
* Install `python-picamera` and `python-netifaces`.
* Install `libav-tools`. This is needed for the `record_calibration` script to convert a raw h264 recording to a MJPEG video for calibration.
* Run `python record_calibration.py front` (or with the other camera) to record a 30-second calibration video named `calibration_front.avi` (or correspondingly named for the other camera) in `~/recordings/calibration_front.avi`.
* Download gdrive from the `gdrive-linux-rpi` binary listed at [prasmussen/gdrive](https://github.com/prasmussen/gdrive) to the Downloads directory. `chmod a+x` it and move it to the home directory and rename it to `gdrive`. In the home directory, run `./gdrive about` and follow the authentication instructions.
* Upload the calibration video to Google Drive: in the home directory, run `./gdrive upload recordings/calibration_front.avi`. Download it on another computer and, on that computer, run [video2calibration](https://github.com/smidm/video2calibration): `python calibrate.py -fs 1 calibration_front.avi calibration_front.yml`; save the calibration results.
* Open `wpa-supplicant`: `sudo vim /etc/wpa_supplicant/wpa_supplicant.conf`. Add a network entry with priority 100 for the `chariot` network, so that the Raspberry Pi preferentially auto-connects to that network when the Tessel 2 server is active:
```
network={
    ssid="chariot"
    key_mgmt=NONE
    priority=100
    id_str="chariot"
}
```
* Copy `start-raspicam` into `/etc/network/if-up.d`. Copy `stop-raspicam` into `/etc/network/if-down.d`. Change the `SIDE` variable in `/etc/network/if-up.d` to be either `front`, `rear`, `left`, or `right`, to indicate the camera.
* Deploy the synchronization server on the Tessel 2 board. The Raspberry Pi should automatically connect to the `chariot` wireless network created by the Tessel 2 server, and the client should automatically start. On the control panel, the board should show up as a connected client. Recordings from the camera will be saved to `~/recordings`, named according to the side the camera is on and the Unix timestamp in the camera's local time.

## Headless File Access
ssh into the Raspberry Pi at the IP address listed on the control panel, using the username `pi`.

