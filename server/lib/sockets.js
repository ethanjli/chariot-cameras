module.exports = function(recording) {
  return {
    connection: function(socket) {
      var client = null;

      console.log('[Sockets] Connection: ' + socket.id);

      socket.on('echo', function(data) {
        console.log('[Sockets] Echo from ' + socket.id, data);
        socket.emit('echo', data);
      });
      socket.on('connected', function(data) {
        client = data.client;
        var clientType = data.clientType;
        socket.join(client);
        if (client === 'control-panel') {
          console.log('[Sockets] Control Panel Initialization: ' + clientType + ' [' + socket.id + ']');
          recording.addControlPanel(socket, clientType);
        } else if (client === 'camera') {
          console.log('[Sockets] Camera Initialization: ' + clientType + ' [' + socket.id + ']');
          recording.addCamera(socket, clientType);
        } else {
          console.log('[Sockets] Unknown client connected', client);
        }
      });
      socket.on('disconnect', function(data) {
        console.log('[Sockets] Disconnection: ' + socket.id);
        if (client === 'control-panel') {
          recording.removeControlPanel(socket.id);
        } else if (client == 'camera') {
          recording.removeCamera(socket.id);
        } else {
          console.log('[Sockets] Unknown client disconnected', client);
        }
      });
    }
  }
};
