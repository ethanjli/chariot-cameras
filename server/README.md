# chariot-cameras server
This contains a Node app which hosts a simple control panel for synchronized control of cameras on separate Raspberry Pi boards, each hosting a camera and running a client.

## Local Hosting
Run `sudo npm start`. Root permissions are required in order to open on port 80. The control panel is then accessible at `localhost/control`

## Heroku Deployment
Push the master branch of the `chariot-cameras` repo up to Heroku. The control panel is then accessible at `http://secret-fortress-28416.herokuapp.com/control`

## Tessel Deployment
WIP

