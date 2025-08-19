import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import bodyParser from 'body-parser';
import cors from 'cors';

// Import serverless handler for reuse locally
import * as contactHandler from '../serverless/contact.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());

// In-memory "DB"
let items = [{ name: 'Sample Item A' }, { name: 'Sample Item B' }];

// Auth endpoints
app.post('/api/login', (req, res) => {
  const { email, password } = req.body || {};
  if (email === 'demo@user.com' && password === 'password123') {
    return res.json({ token: 'mock-jwt-token', user: { email } });
  }
  return res.status(401).json({ error: 'Invalid credentials' });
});

app.get('/api/me', (req, res) => {
  const auth = req.headers.authorization || '';
  if (auth.startsWith('Bearer ')) {
    return res.json({ email: 'demo@user.com' });
  }
  return res.status(401).json({ error: 'Unauthorized' });
});

// Items
app.get('/api/items', (req, res) => {
  const auth = req.headers.authorization || '';
  if (!auth.startsWith('Bearer ')) return res.status(401).json({ error: 'Unauthorized' });
  return res.json(items);
});
app.post('/api/items', (req, res) => {
  const auth = req.headers.authorization || '';
  if (!auth.startsWith('Bearer ')) return res.status(401).json({ error: 'Unauthorized' });
  const { name } = req.body || {};
  if (!name || !String(name).trim()) return res.status(400).json({ error: 'Name required' });
  const created = { name: String(name).trim() };
  items.push(created);
  return res.status(201).json(created);
});

// Contact: reuse serverless handler
app.post('/api/contact', async (req, res) => {
  try {
    const response = await contactHandler.handler({ body: JSON.stringify(req.body || {}) });
    res.status(response.statusCode || 200).type('application/json').send(response.body);
  } catch (err) {
    res.status(500).json({ error: 'Server error', details: err.message });
  }
});

// Static site
const publicRoot = path.resolve(__dirname, '..');
app.use(express.static(publicRoot, { extensions: ['html'] }));

app.listen(PORT, () => {
  console.log(`Dev server running at http://localhost:${PORT}`);
});
