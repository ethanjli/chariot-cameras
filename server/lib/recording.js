var _ = require('lodash');
var moment = require('moment')

module.exports = function(socketio) {
  var recordingTimer = null;
  var controlPanels = {};
  var cameras = {};
  var clients = {};
  var state = 'ready';
  var startTime = null;
  var stopTime = null;
  var events = [];

  // Client management
  function controlPanelsRoom() {
    return socketio.to('control-panel');
  }
  function camerasRoom() {
    return socketio.to('camera');
  }
  function numControlPanels() {
    return Object.keys(controlPanels).length;
  }
  function numCameras() {
    return Object.keys(cameras).length;
  }

  // Recording synchronization
  function isRecording() {
    return startTime !== null;
  }
  function startRecording() {
      if (startTime !== null) {
        return;
      }
      if (startTime === null) {
        startTime = moment();
      }
      console.log('[Recording] Starting recording.');
      state = 'running';
      controlPanelsRoom().emit('start');
      camerasRoom().emit('start');
      logEvent({name: 'start-recording'});
  }
  function stopRecording() {
      if (startTime === null || stopTime !== null) {
        return;
      }
      stopTime = moment();
      console.log('[Recording] Stopping recording.');
      state = 'stopped';
      controlPanelsRoom().emit('stop');
      logEvent({name: 'stop-recording'});
  }
  function resetRecording() {
      stopRecording();
      console.log('[Recording] Resetting recording.');
      state = 'ready';
      events = [];
      controlPanelsRoom().emit('reset');
      camerasRoom().emit('reset');
      startTime = null;
      stopTime = null;
  }

  // Event logging
  function logEvent(newEvent) {
    console.log('[Recording] Logging event:', newEvent);
    events.push(_.assign(newEvent, {time: moment()}));
  }

  // Camera control
  function shutdownCameras() {
    console.log('[Recording] Sending shutdown to cameras');
    camerasRoom().emit('shutdown');
  }

  // Public interface
  return {
    // Management of clients
    addControlPanel: function(socket, clientType) {
      controlPanels[socket.id] = socket;
      clients[socket.id] = clientType;
      socket.emit('camera-connection-info', numCameras());
      socket.emit('recording-state-info', state);
      socket.on('start', startRecording);
      socket.on('reset', resetRecording);
      socket.on('stop', stopRecording);
      socket.on('event', logEvent);
      socket.on('shutdown', shutdownCameras);
      controlPanelsRoom().emit('control-connection-info', numControlPanels());
    },
    addCamera: function(socket, clientType) {
      cameras[socket.id] = socket;
      clients[socket.id] = clientType;
      controlPanelsRoom().emit('camera-connection-info', numCameras());
    },
    removeControlPanel: function(socketId) {
      delete controlPanels[socketId];
      delete clients[socketId];
      if (numControlPanels() === 0 && numCameras() == 0 && isRecording()) {
        stopRecording();
      }
      controlPanelsRoom().emit('control-connection-info', numControlPanels());
    },
    removeCamera: function(socketId) {
      delete cameras[socketId];
      delete clients[socketId];
      if (numControlPanels() === 0 && numCameras() == 0 && isRecording()) {
        stopRecording();
      }
      controlPanelsRoom().emit('camera-connection-info', numCameras());
    },
    getStartTime: function() {
      return startTime;
    },
    getStopTime: function() {
      return stopTime;
    },
    getEvents: function() {
      return events;
    },
    getClients: function() {
      return _.values(clients);
    }
  };
}
