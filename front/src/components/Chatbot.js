import React, { useState } from 'react';

// Paleta:
// Fondo: #3C4959
// Barra: #A69581
// Botón: #59443F
// Texto: #202026

const ChatLanding = () => {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    // Simulación de respuesta (aquí iría la llamada real al backend)
    setTimeout(() => {
      setResponse(`Echo: ${input}`);
      setLoading(false);
    }, 800);
    setInput('');
  };

  return (
    <>
      <style>
        {`
          * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
          }
          body {
            margin: 0;
            padding: 0;
            overflow-x: hidden;
          }
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        `}
      </style>
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        background: '#3C4959',
        margin: 0,
        padding: 0,
        width: '100vw',
        height: '100vh',
      }}>
        <h1 style={{ 
          fontWeight: 800, 
          fontSize: 48, 
          marginBottom: 64, 
          color: '#A69581',
          margin: 0,
          fontFamily: 'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          letterSpacing: '-0.025em',
          lineHeight: 1.1,
        }}>
          Chatbot Turing Challenge
        </h1>
        <div style={{
          display: 'flex',
          maxWidth: 700,
          width: '100%',
          background: '#A69581',
          borderRadius: 32,
          padding: 8,
          marginBottom: 24,
        }}>
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="Haz tu pregunta..."
            style={{
              flex: 1,
              border: 'none',
              outline: 'none',
              fontSize: 20,
              padding: '16px 20px',
              borderRadius: 32,
              background: 'transparent',
              color: '#202026',
            }}
          />
          <button
            onClick={handleSend}
            disabled={loading}
            style={{
              border: 'none',
              background: '#59443F',
              color: '#A69581',
              borderRadius: 32,
              padding: '0 32px',
              fontSize: 20,
              cursor: 'pointer',
              fontWeight: 600,
              marginLeft: 8,
            }}
          >
            {loading ? '...' : 'Enviar'}
          </button>
        </div>
        {response && (
          <div style={{
            maxWidth: 700,
            background: '#A69581',
            borderRadius: 16,
            padding: 24,
            fontSize: 20,
            color: '#202026',
          }}>
            {response}
          </div>
        )}
      </div>
    </>
  );
};

export default ChatLanding; 