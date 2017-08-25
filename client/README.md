# chariot-cameras clients
This contains various Python clients to connect to the `chariot-cameras` server.

## Test Client
This is a test client useful for testing connections to the server. Run `python3 test-client.py --server local` to connect to a local server, or substitute `local` with `heroku` or `tessel` to connect to the servers deployed on Heroku or Tessel, respectively.

## Raspberry Pi Camera Client
This is an actual client intended for headless deployment on a Raspberry Pi board with a wi-fi connection to a Tessel board running the `chariot-cameras` server as a wireless access point. Run `python raspicam.py front` to run the client as the controller for the front camera, or substitute `front` with `left`, `right`, or `rear` to run the client as a controller for the left, right, or rear cameras, respectively. To connect to the Heroku server, add `--server heroku`. To make shutdown simply quit the program rather than halting the entire computer, add `--quit`.

## Raspberry Pi Deployment Setup
Assuming the Raspberry Pi board is a Raspberry Pi Zero W running a preloaded NOOBS:
* Let NOOBS install Raspbian on the SD card.
* Install all updates with `sudo apt-get update` and `sudo apt-get upgrade`.
* Run the "Raspberry Pi Configuration" graphical program. In the "Interfaces" tab, enable the Camera.
* Open the terminal. In the home directory, clone this repo as `git clone https://github.com/ethanjli/chariot-cameras.git`.
* Install the `socketIO-client` module as `sudo pip install socketIO-client`.
* Install `python-picamera`.

