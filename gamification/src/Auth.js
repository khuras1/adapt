import React, { useState } from 'react';
import { supabase } from './supabaseClient';

export default function Auth() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handleSignUp = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');
    const { error } = await supabase.auth.signUp({ email, password });
    if (error) setError(error.message);
    else setMessage('Check your email for a confirmation link!');
    setLoading(false);
  };

  const handleSignIn = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) setError(error.message);
    else setMessage('Signed in!');
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 320, margin: 'auto', padding: 32 }}>
      <h2>Sign Up / Sign In</h2>
      <form>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          style={{ width: '100%', marginBottom: 8 }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          style={{ width: '100%', marginBottom: 8 }}
        />
        <button onClick={handleSignUp} disabled={loading} style={{ width: '100%', marginBottom: 8 }}>
          Sign Up
        </button>
        <button onClick={handleSignIn} disabled={loading} style={{ width: '100%' }}>
          Sign In
        </button>
      </form>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
      {message && <div style={{ color: 'green', marginTop: 8 }}>{message}</div>}
    </div>
  );
}
