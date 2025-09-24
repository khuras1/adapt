// gamificationAgent.js
// Example React agent module to enable gamification using Gemini API via backend proxy

export async function getGamificationSuggestion(prompt) {
  const response = await fetch('/api/gemini', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt })
  });
  if (!response.ok) throw new Error('Failed to fetch from Gemini agent');
  const data = await response.json();
  // Parse Gemini response as needed
  return data;
}

// Example usage:
// getGamificationSuggestion('Suggest a fun group challenge for students')
//   .then(data => console.log(data))
//   .catch(err => console.error(err));
