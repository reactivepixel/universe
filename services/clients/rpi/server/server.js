const express = require('express');
const bodyParser = require('body-parser');
const PythonShell = require('python-shell');
const path = require("path");


const app = express();

const port = process.env.PORT || 3000;

app.use(bodyParser.json());

app.get('/clear', (req, res) => {

  pyShell.end((err) => {
  if (err) throw err;
    console.log('ending pyShell');
  });


  const scriptPath = './py_ctrl/clear.py';
  PythonShell.run(scriptPath, (err) => {
    if (err) throw err;
    console.log('Success: ran py script');
  });

  res.status(200).json(scriptPath);
});


app.get('/test', (req, res) => {
  const scriptPath = './py_ctrl/test.py';
  PythonShell.run(scriptPath, (err) => {
    if (err) throw err;
    console.log('Success: ran py script');
  });

  res.status(200).json(scriptPath);
});

app.use('/', (req, res) => {
  res.status(200).json({ healthy: true });
});



// Activate on Start
const startPath = './py_ctrl/start.py';

pyShell = new PythonShell(startPath);
//
// PythonShell.run(startPath, (err) => {
//   if (err) throw err;
//   console.log('Success: ran py script');
// });


exports.server = app.listen(port, () => {
  console.log('Server Active On Port', port);
});
