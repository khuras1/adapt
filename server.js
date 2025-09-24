// server.js
// Node.js/Express backend proxy for Gemini API (secure your API key!)
const express = require('express');
const axios = require('axios');
require('dotenv').config();
const app = express();
app.use(express.json());

const GEMINI_API_KEY = process.env.REACT_APP_GEMINI_API_KEY;
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';

app.post('/api/gemini', async (req, res) => {
  try {
    const { prompt } = req.body;
    const response = await axios.post(
      `${GEMINI_API_URL}?key=${GEMINI_API_KEY}`,
      { contents: [{ parts: [{ text: prompt }] }] }
    );
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 5001;
app.listen(PORT, () => console.log(`Gemini proxy running on port ${PORT}`));
