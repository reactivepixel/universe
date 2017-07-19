var mosca = require('mosca');
const util = require('apex-util');

var ascoltatore = {
  //using ascoltatore
  type: 'mongo',
  url: 'mongodb://localhost:27017/mqtt',
  pubsubCollection: 'universe',
  mongo: {}
};
var settings = {
  port: parseInt(process.env.MQTT_PORT, 10),
  backend: ascoltatore
};

var server = new mosca.Server(settings);

server.on('clientConnected', function(client) {
    util.log('[Broker Event] Client Connected', client.id);
});

// fired when a message is received
server.on('published', function(packet, client) {
  util.log('[Broker Event] Msg Published', packet.payload, 3);
});

server.on('ready', setup);

server.on('clientDisconnecting', function (client) {
    util.log('[Broker Event] Client Disconnecting', client.id);
});

server.on('clientDisconnected', function (client) {
    util.log('[Broker Event] Client Disconnected', client.id);
});

// fired when the mqtt server is ready
function setup() {
  util.log('[Broker Event] MQTT Broker Active on port', process.env.MQTT_PORT);
}
