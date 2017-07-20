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

  router.get('/clear', (req, res) => {
    const clearCmd = { action: 'clear' };

    safePublish('lobby', JSON.stringify(clearCmd), mqClient);
    res.send('confirmed: Clear');
  });

  router.get('/test', (req, res) => {
    const cmd = { action: 'test' };

    safePublish('lobby', JSON.stringify(cmd), mqClient);
    res.send('confirmed: Clear');
  });

  router.get('/info', (req, res) => {
    const cmd = { action: 'info' };

    safePublish('lobby', JSON.stringify(cmd), mqClient);
    res.send('confirmed: Clear');
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
