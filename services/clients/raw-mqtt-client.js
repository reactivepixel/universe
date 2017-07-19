var mqtt = require('mqtt')

var client  = mqtt.connect(process.env.MQTT_CONN_STR);

client.on('connect', function () {
  client.subscribe('lobby');
  // client.subscribe('bkDoor');
  // client.subscribe(process.env.DEVICE_ID);

  // client.publish('presence', 'Hello mqtt', callback)
  // client.publish('lobby', 'Hello mqtt')
})

// client.on('message', function (topic, message) {
//   // message is Buffer
//   console.log(message.toString())
//   // client.end()
// })

// client.publish('presence', 'shhhh, im here');
// // client.end();
//
// client.publish('ctrl', '{healthy:true}', { qos: 1});
// client.publish('ctrl', '{healthy:true}', { qos: 1});
// client.publish('ctrl', '{healthy:true}', { qos: 1});
// client.publish('ctrl', '{healthy:true}', { qos: 1});
// client.publish('ctrl', '{healthy:true}', { qos: 1});
// client.publish('ctrl', '{healthy:true}', { qos: 1});
