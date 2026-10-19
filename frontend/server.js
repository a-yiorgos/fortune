const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const rawBackendUrl = process.env.BACKEND_URL || 'http://127.0.0.1:8000';
// Remove trailing slash if present for clean URL concatenation
const BACKEND_URL = rawBackendUrl.replace(/\/+$/, '');

app.get('/config.js', (req, res) => {
  res.type('application/javascript');
  res.send(`window.BACKEND_URL = ${JSON.stringify(BACKEND_URL)};`);
});

app.use(express.static(path.join(__dirname, 'public')));

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Frontend server listening on port ${PORT}`);
  console.log(`Configured backend URL: ${BACKEND_URL}`);
});
