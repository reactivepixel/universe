var mqtt = require('mqtt')

const connString = 'mqtt://localhost:1883'

var client  = mqtt.connect(connString);

client.on('connect', function () {
  client.subscribe('presence')
  client.subscribe('ctrl')
  // client.publish('presence', 'Hello mqtt', callback)
  client.publish('presence', 'Hello mqtt')
})

client.on('message', function (topic, message) {
  // message is Buffer
  console.log(message.toString())
  // client.end()
})

// client.publish('presence', 'shhhh, im here');
// client.end();

client.publish('ctrl', '{healthy:true}', { qos: 1});
client.publish('ctrl', '{healthy:true}', { qos: 1});
client.publish('ctrl', '{healthy:true}', { qos: 1});
client.publish('ctrl', '{healthy:true}', { qos: 1});
client.publish('ctrl', '{healthy:true}', { qos: 1});
client.publish('ctrl', '{healthy:true}', { qos: 1});
