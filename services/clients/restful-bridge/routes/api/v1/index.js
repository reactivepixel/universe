const express = require('express');

module.exports = (mqClient) => {
  const router = express.Router();

  router.get('/status', (req, res) => {
    res.json({
      mqtt_client_status: mqClient.connected,
    });
  });

  router.get('/close', (req, res) => {
    mqClient.end();
    res.send('client closed')
  });

  router.post('/:action', (req, res) => {
    const cmd = req.body;
    cmd.success = true;
    safePublish('lobby', JSON.stringify(cmd), mqClient);
    res.json(cmd);
  });
  return router;
};

function safePublish(room, msg, client){
  if(client.connected){
    client.publish(room, msg);
  } else {
    console.log('not connected');
  }
}
