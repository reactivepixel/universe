module.exports = (express) => {
  const router = express.Router();

  // Middleware
  router.use((req, res, next) => {
    console.log({
      action: 'Incoming Request',
      route: req.originalUrl,
      body: req.body,
    })

    // Run Next Route
    next()
  })

  // Status Route
  router.get('/status', (req, res) => {
    res.json({
      healthy: true,
    });
  });

  // Routes
  router.use('/ctrl/', require('./ctrl')(express));

  return router;
};
