# chariot-cameras server
This contains a Node app which hosts a simple control panel for synchronized control of cameras on separate Raspberry Pi boards, each hosting a camera and running a client.

## Local Hosting
Run `sudo npm start`. Root permissions are required in order to open on port 80. The control panel is then accessible at `localhost/control`

## Heroku
### Setup
Make a new Node.js app. The project is currently using `secret-fortress-28416.herokuapp.com`.
### Deployment
Push the master branch of the `chariot-cameras` repo up to Heroku. The control panel is then accessible at `http://secret-fortress-28416.herokuapp.com/control`

## Tessel Deployment
### Setup
Install `nvm`. Using, NVM, install Node.js 4.8 as `nvm install 4.8`. Use Node.js 4.8 as `nvm use 4.8`.
Install `libusb` and `libudev`.
Install the Tessel 2 CLI as `npm install -g t2-cli`. Install the drivers as `sudo t2 install drivers`.
Plug the Tessel 2 board in, then run `t2 list`. The board should be listed.
Configure the board to host a wireless access point: `t2 wifi --off` and `t2 ap -n chariot`, then `t2 ap --on`.
### Deployment
Run `t2 push app.js`. You can then access the control panel at `192.168.1.101`.

