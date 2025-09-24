import React, { useState } from 'react';

const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';
const GEMINI_API_KEY = process.env.REACT_APP_GEMINI_API_KEY; // Store your key in .env

export default function GamificationChatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages([...messages, { sender: 'user', text: input }]);
    setLoading(true);
    try {
      const res = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: input }] }]
        })
      });
      const data = await res.json();
      const aiText = data.candidates?.[0]?.content?.parts?.[0]?.text || 'No response.';
      setMessages((msgs) => [...msgs, { sender: 'ai', text: aiText }]);
    } catch (err) {
      setMessages((msgs) => [...msgs, { sender: 'ai', text: 'Error contacting Gemini API.' }]);
    }
    setInput('');
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 400, margin: 'auto', padding: 16 }}>
      <h3>Quiz Gamification Chatbot</h3>
      <div style={{ minHeight: 120, border: '1px solid #ccc', padding: 8, marginBottom: 8 }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ color: msg.sender === 'user' ? '#333' : '#007bff' }}>
            <b>{msg.sender === 'user' ? 'You' : 'AI'}:</b> {msg.text}
          </div>
        ))}
        {loading && <div>AI is typing...</div>}
      </div>
      <form onSubmit={sendMessage} style={{ display: 'flex', gap: 8 }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask about quiz gamification..."
          style={{ flex: 1 }}
        />
        <button type="submit" disabled={loading || !input.trim()}>Send</button>
      </form>
    </div>
  );
}
