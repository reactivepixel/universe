const express = require('express');

module.exports = () => {
  const router = express.Router();

  router.get('/status', (req, res) => {
    res.json({
      hello: true,
    });
  });


  router.get('/', (req, res) => {
    res.render('dashboard');
  });

  return router;
};
