
const PythonShell = require('python-shell');
const ctrl = require('../models/ctrl');

module.exports = (express) => {
  const router = express.Router();

  router.get('/dual', (req, res) => {
    const scriptPath = './server/dual.py';
    PythonShell.run(scriptPath, (err) => {
      if (err) throw err;
      console.log('Success: ran py script');
    });

    res.status(200).json(scriptPath);
  });

  router.get('/clear', (req, res) => {
    const scriptPath = './server/clear.py';
    PythonShell.run(scriptPath, (err) => {
      if (err) throw err;
      console.log('Success: ran py script');
    });

    res.status(200).json(scriptPath);
  });




  // Strand(s) test
  router.get('/test', (req, res) => ctrl.test(req, res));

  return router;
};
