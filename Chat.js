import React, { useState, useRef, useEffect } from "react";
import "./Chat.css";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const bottomRef = useRef(null);

  // Auto-scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage() {
    if (!input.trim()) return;

    // Push user message
    const userMsg = {
      sender: "user",
      text: input,
      time: new Date().toLocaleTimeString(),
    };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();

      // FIXED: Server ALWAYS sends `message` (string)
      const botText =
        typeof data.message === "string"
          ? data.message
          : "⚠️ Error: Invalid response from server";

      const botMsg = {
        sender: "bot",
        text: botText,
        time: new Date().toLocaleTimeString(),
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "⚠️ Backend unreachable.",
          time: new Date().toLocaleTimeString(),
        },
      ]);
    }

    setInput("");
  }

  return (
    <div className="chat-wrapper">
      <h1 className="chat-title">Medical Assistant Chat</h1>

      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`msg-row ${msg.sender}`}>
            <div className="msg-bubble">{msg.text}</div>
            <div className="msg-time">{msg.time}</div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}
