const mqtt = require('mqtt');
const express = require('express');
const bodyParser = require('body-parser');

const util = require('apex-util');

const subRooms = {
  'lobby': 'lobby',
  'master': 'bkDoor',
  'device': process.env.DEVICE_ID,
  'group': process.env.GROUP_ID,
  'venue': process.env.VENUE_ID,
};

// Express Config
const app = express();

const port = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true,
}));


// Activate MQTT client
const mqClient  = mqtt.connect(process.env.MQTT_CONN_STR);

mqClient.on('connect', () => {
  const roomKeys = Object.keys(subRooms);
  for(roomKey in roomKeys){
    let room = subRooms[roomKeys[roomKey]];

    util.log('[Client Event] Subscribe to Room', room);
    mqClient.subscribe(room);
  }
  mqClient.publish(subRooms.lobby, 'Have I arrived too late?');
});

mqClient.on('message', function (topic, message) {
  // message is Buffer
  util.log('[Client Event] MQTT Message Recieved', message.toString());
  // client.end()
})

// Connect mqtt Client to Express
app.use('/ctrl', require('./routes')(mqClient));


// Activate Express Server
exports.server = app.listen(port, () => {
  util.log('[Client Event] Restful-Bridge Server Active On Port', 'http://' + process.env.HOST + ':' + port);
});




// =========
// On Server Closing
// =========

process.stdin.resume();//so the program will not close instantly

function exitHandler(options, err) {
    if (options.cleanup) console.log('clean');
    if (err) console.log(err.stack);
    if (options.exit) {
      mqClient.end();
      console.log('ended client');
      process.exit();
    }
}

//do something when app is closing
process.on('exit', exitHandler.bind(null,{cleanup:true}));

//catches ctrl+c event
process.on('SIGINT', exitHandler.bind(null, {exit:true}));

//catches uncaught exceptions
process.on('uncaughtException', exitHandler.bind(null, {exit:true}));
