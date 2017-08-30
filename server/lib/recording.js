var _ = require('lodash');
var moment = require('moment')

module.exports = function(socketio) {
  var recordingTimer = null;
  var controlPanels = {};
  var cameras = {};
  var clients = {};
  var ipAddresses = {};
  var state = 'ready';
  var startTime = null;
  var stopTime = null;
  var events = [];

  function getPSTTime(time) {
    return time.toLocaleString('en-US', {
      timeZone: 'PST',
      timeZoneName: 'short'
    });
  }

  function getUnixTime(time) {
    return time.valueOf()
  }

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
  function cameraTypes() {
    return _.values(_.pick(clients, _.keys(cameras)));
  }
  function cameraIpAddresses() {
    return _.values(_.pick(ipAddresses, _.keys(cameras)));
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
  }
  function stopRecording() {
      if (startTime === null || stopTime !== null) {
        return;
      }
      stopTime = moment();
      console.log('[Recording] Stopping recording.');
      state = 'stopped';
      controlPanelsRoom().emit('stop');
      camerasRoom().emit('stop');
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
    var currentTime = moment()
    events.push(_.assign(newEvent, {
      'eventTime': {
        'iso': currentTime,
        'local': getPSTTime(currentTime),
        'unix': getUnixTime(currentTime)
      }
    }));
  }

  // Camera control
  function shutdownCameras() {
    console.log('[Recording] Sending shutdown to cameras');
    camerasRoom().emit('shutdown');
  }

  // Public interface
  return {
    getPSTTime: getPSTTime,
    getUnixTime: getUnixTime,
    // Management of clients
    addControlPanel: function(socket, clientType, metadata) {
      controlPanels[socket.id] = socket;
      clients[socket.id] = clientType;
      socket.emit('camera-connection-info', {
        'number': numCameras(),
        'clients': cameraTypes(),
        'ipAddresses': cameraIpAddresses()
      });
      socket.emit('recording-state-info', state);
      socket.on('start', startRecording);
      socket.on('reset', resetRecording);
      socket.on('stop', stopRecording);
      socket.on('event', logEvent);
      socket.on('shutdown', shutdownCameras);
    },
    addCamera: function(socket, clientType, metadata) {
      cameras[socket.id] = socket;
      clients[socket.id] = clientType;
      if (metadata !== undefined) {
        ipAddresses[socket.id] = metadata.ip;
      }
      console.log(cameraIpAddresses());
      controlPanelsRoom().emit('camera-connection-info', {
        'number': numCameras(),
        'clients': cameraTypes(),
        'ipAddresses': cameraIpAddresses()
      });
      socket.on('event', logEvent);
      logEvent({
        'name': 'cameraConnected',
        'connected': clientType,
        'all': cameraTypes()
      });
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
      var cameraName = clients[socketId];
      delete cameras[socketId];
      delete clients[socketId];
      if (numControlPanels() === 0 && numCameras() == 0 && isRecording()) {
        stopRecording();
      }
      console.log(cameraIpAddresses());
      controlPanelsRoom().emit('camera-connection-info', {
        'number': numCameras(),
        'clients': cameraTypes(),
        'ipAddresses': cameraIpAddresses()
      });
      logEvent({
        'name': 'cameraDisconnected',
        'disconnected': cameraName,
        'all': cameraTypes()
      });
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
