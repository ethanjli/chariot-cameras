var express = require('express');
var http = require('http');

var path = require('path');
var logger = require('morgan');

var app = express();
var port = process.env.PORT || 80;
var server = http.Server(app);
var socketio = require('socket.io')(server)
server.listen(port, function() {
  console.log('[Server] Listening on port %d in %s mode', port, app.settings.env);
});

var recording = require('./lib/recording')(socketio);
var sockets = require('./lib/sockets')(recording);

//app.use(logger('dev'));
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', function(req, res) {
  res.sendFile(path.join(__dirname, 'public', 'index.html'))
});
app.get('/display', function(req, res) {
  res.sendFile(path.join(__dirname, 'public', 'display-panel.html'))
});
app.get('/control-display', function(req, res) {
  res.sendFile(path.join(__dirname, 'public', 'control-display-panel.html'))
});
app.get('/minimal-display', function(req, res) {
  res.sendFile(path.join(__dirname, 'public', 'minimal-display-panel.html'))
});
app.get('/control', function(req, res) {
  res.sendFile(path.join(__dirname, 'public', 'control-panel.html'))
});
app.get('/scenario-ideal', function(req, res) {
  res.sendFile(path.join(__dirname, 'public', 'scenario-ideal.html'))
});
app.get('/scenario-extreme', function(req, res) {
  res.sendFile(path.join(__dirname, 'public', 'scenario-extreme.html'))
});
app.get('/json', function(req, res) {
  if (recording.getStartTime() === null) {
    res.sendStatus(204);
    return;
  }
  var startTime = recording.getStartTime().format('YYYYMMDD-HHmmss');
  res.set({
    'Content-Disposition': 'attachment; filename=recording_' + startTime + '.json',
    'Content-Type': 'application/json'
  });
  var json = JSON.stringify({
    startTime: {
      iso: recording.getStartTime(),
      local: recording.getPSTTime(recording.getStartTime()),
      unix: recording.getUnixTime(recording.getStartTime())
    },
    stopTime: {
      iso: recording.getStopTime(),
      local: recording.getPSTTime(recording.getStopTime()),
      unix: recording.getUnixTime(recording.getStopTime())
    },
    events: recording.getEvents(),
    clients: recording.getClients()
  }, null, '  ');
  res.send(json);
});
app.get('/favicon.ico', function(req, res) {
  res.sendStatus(200);
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// production error handler, no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  next(err);
});

socketio.on('connection', sockets.connection);
