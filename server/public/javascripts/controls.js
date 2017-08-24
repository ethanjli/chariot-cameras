var RecordingBehavior = new machina.BehavioralFsm({
    namespace: 'Recording',
    initialState: 'ready',
    states: {
        ready: {
            _onEnter: function(client) {
                client.startResetBtn.innerHTML = 'Start';
                client.startResetBtn.disabled = '';
            },
            start: 'running',
            stop: 'stopped',
            clickStartReset: function(client) {
                this.transition(client, 'waitingForResponse');
                client.socket.emit('start');
            },
            disconnectSocket: 'waitingForResponse'
        },
        running: {
            _onEnter: function(client) {
                client.startResetBtn.innerHTML = 'Stop';
            },
            reset: 'ready',
            stop: 'stopped',
            clickStartReset: function(client) {
                this.transition(client, 'waitingForResponse');
                client.socket.emit('stop');
            },
            disconnectSocket: 'waitingForResponse'
        },
        stopped: {
            _onEnter: function(client) {
                client.startResetBtn.innerHTML = 'Reset';
            },
            reset: 'ready',
            start: 'running',
            clickStartReset: function(client) {
                this.transition(client, 'waitingForResponse');
                client.socket.emit('reset');
            },
            disconnectSocket: 'waitingForResponse'
        },
        waitingForResponse: {
            _onEnter: function(client) {
                client.startResetBtn.disabled = 'disabled';
            },
            _onExit: function(client) {
                client.startResetBtn.disabled = '';
            },
            reset: 'ready',
            start: 'running',
            stop: 'stopped'
        }
    },
    reset: function(client) {
        this.handle(client, 'reset');
    },
    start: function(client) {
        this.handle(client, 'start');
    },
    stop: function(client) {
        this.handle(client, 'stop');
    },
    clickStartReset: function(client) {
        this.handle(client, 'clickStartReset');
    },
    disconnectSocket: function(client) {
        this.handle(client, 'disconnectSocket');
    }
});
function Recording(options) {
    this.socket = options.socket;
    this.startResetBtn = document.getElementById(options.startResetBtn);
    this.initializationTime = options.initializationTime;

    this.listen();
    this.monitor();
}
Recording.prototype.listen = function() {
    this.socket.on('start', (function() {
        console.log('Sockets: Starting recording.');
        RecordingBehavior.start(this);
    }).bind(this));
    this.socket.on('reset', (function() {
        console.log('Sockets: Resetting recording.');
        RecordingBehavior.reset(this);
    }).bind(this));
    this.socket.on('stop', (function() {
        console.log('Sockets: Stopping recording.');
        RecordingBehavior.stop(this);
    }).bind(this));
    this.socket.on('recording-state-info', (function(data) {
        console.log('Sockets: Recording state is: ' + data);
        if (data === 'ready') RecordingBehavior.reset(this);
        else if (data === 'running') RecordingBehavior.start(this);
        else if (data === 'stopped') RecordingBehavior.stop(this);
    }).bind(this));
    this.socket.on('disconnect', RecordingBehavior.disconnectSocket.bind(RecordingBehavior, this));
}
Recording.prototype.monitor = function() {
    this.startResetBtn.onclick = RecordingBehavior.clickStartReset.bind(RecordingBehavior, this);
}

function SocketConnection(options) {
    this.clientType = options.clientType;
    this.connectionStatusElem = document.getElementById(options.connectionStatusElem);
    this.cameraStatusElem = document.getElementById(options.cameraStatusElem);
    this.socket = options.socket;
    this.listen();
}
SocketConnection.prototype.listen = function() {
    this.socket.on('connect', this.connected.bind(this));
    this.socket.on('control-connection-info', this.multipleConnected.bind(this));
    this.socket.on('camera-connection-info', this.cameraConnected.bind(this));
    this.socket.on('disconnect', this.disconnected.bind(this));
}
SocketConnection.prototype.connected = function() {
    this.multipleConnected(1);
    console.log('Sockets: Connected to server.');
    this.socket.emit('connected', {client: 'control-panel', clientType: this.clientType});
}
SocketConnection.prototype.disconnected = function() {
    this.connectionStatusElem.innerHTML = 'Not connected to server';
    this.connectionStatusElem.className = 'label label-danger';
    console.log('Sockets: Disconnected from server.');
}
SocketConnection.prototype.multipleConnected = function(numControlPanels) {
    if (numControlPanels === 1) {
        this.connectionStatusElem.innerHTML = 'Connected to server';
        this.connectionStatusElem.className = 'label label-success';
        return;
    }
    this.connectionStatusElem.innerHTML = numControlPanels + ' control panels connected to server';
    this.connectionStatusElem.className = 'label label-info';
}
SocketConnection.prototype.cameraConnected = function(numCameraInterfaces) {
    if (numCameraInterfaces === 0) {
        this.cameraStatusElem.innerHTML = 'No cameras connected to server';
        this.cameraStatusElem.className = 'label label-warning';
        return;
    }
    this.cameraStatusElem.innerHTML = numCameraInterfaces + ' cameras connected to server';
    if (numCameraInterfaces === 4) {
        this.cameraStatusElem.className = 'label label-success';
    } else {
        this.cameraStatusElem.className = 'label label-info';
    }
}

