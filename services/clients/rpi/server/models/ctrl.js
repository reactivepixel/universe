const PythonShell = require('python-shell');

exports.test = (req, res) => {

  // Args
  var options = {
    mode: 'text',
    pythonPath: '/usr/bin/python',
    pythonOptions: ['-u'],
    scriptPath: './server/',
    args: ['value1', 'value2', 'value3']
  };

  PythonShell.run('test.py', options, (err, results) => {
    if (err) res.status(500).json(err);
    console.log(results);
    res.status(200).json(results);
  });

}

// router.get('/dual', (req, res) => {
//   const scriptPath = './server/dual.py';
//   PythonShell.run(scriptPath, (err) => {
//     if (err) throw err;
//     console.log('Success: ran py script');
//   });
//
//   res.status(200).json(scriptPath);
// });
