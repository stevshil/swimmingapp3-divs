const express = require('express');
const apiMocker = require('connect-api-mocker');

const port = 9000;
const app = express();
const cors = require('cors')
 
// app.use('/api', apiMocker('mock-api'));
app.use(cors())
app.use('/', apiMocker('.'))
// First argument is the endpoint for entry
// Second argument is the directory where the JSON files are
 
console.log(`Mock API Server is up and running at: http://localhost:${port}`);
app.listen(port);