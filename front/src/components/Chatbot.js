import React, { useState, useRef, useEffect } from 'react';

// Paleta:
// Fondo: #3C4959
// Barra: #A69581
// Botón: #59443F
// Texto: #202026

const ChatLanding = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]); // historial de mensajes
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const API_URL = 'http://localhost:8000/chat';

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input }),
      });
      const data = await res.json();
      const botMessage = { sender: "bot", text: data.response };
      if (data.image_base64) {
        botMessage.image_base64 = data.image_base64;
        console.log("[FRONT] Imagen base64 recibida", data.image_base64.slice(0, 30) + '...');
      }
      if (typeof data.rag_used !== 'undefined') {
        botMessage.rag_used = data.rag_used;
      }
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Error al conectar con el backend: " + err.message },
      ]);
    }
    setLoading(false);
  };

  // Autoscroll al último mensaje
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

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
        justifyContent: 'flex-start',
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
          marginBottom: 120,
          color: '#A69581',
          marginTop: 40,
          marginLeft: 0,
          marginRight: 0,
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
          marginBottom: 40,
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
        {/* Historial de mensajes tipo chat */}
        <div style={{
          maxWidth: 700,
          width: '100%',
          background: '#3C4959',
          borderRadius: 16,
          padding: 24,
          fontSize: 20,
          color: '#A69581',
          minHeight: 200,
          display: 'flex',
          flexDirection: 'column',
          gap: 16,
          overflowY: 'auto',
          height: 400,
        }}>
          {messages.map((msg, idx) => (
            <div key={idx} style={{
              alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
              background: 'transparent',
              color: '#A69581',
              borderRadius: 16,
              padding: '12px 20px',
              maxWidth: '80%',
              marginBottom: 4,
              fontWeight: 500,
              fontFamily: 'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
              display: 'flex',
              alignItems: 'center',
              gap: 8,
            }}>
              {msg.sender === 'user' ? 'Tú: ' : 'Bot: '}
              {msg.sender === 'bot' && (
                <span title={msg.rag_used === true ? 'Respuesta basada en la base de datos' : msg.rag_used === false ? 'Respuesta solo del modelo' : ''} style={{ marginRight: 6, fontSize: 22 }}>
                  {msg.rag_used === true ? '📚' : msg.rag_used === false ? '💬' : ''}
                </span>
              )}
              {msg.text}
              {msg.image_base64 && (
                <img
                  src={`data:image/png;base64,${msg.image_base64}`}
                  alt="Imagen relacionada"
                  style={{ maxWidth: "300px", marginLeft: 8, borderRadius: 8 }}
                />
              )}
            </div>
          ))}
          {loading && (
            <div style={{
              alignSelf: 'flex-end',
              background: 'transparent',
              color: '#A69581',
              borderRadius: 16,
              padding: '12px 20px',
              maxWidth: '80%',
              marginBottom: 4,
              fontWeight: 500,
              fontFamily: 'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
              display: 'flex',
              alignItems: 'center',
              gap: 8,
            }}>
              <span style={{ marginRight: 6, fontSize: 22 }}>🤔</span>Pensando...
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
    </>
  );
};

export default ChatLanding; 