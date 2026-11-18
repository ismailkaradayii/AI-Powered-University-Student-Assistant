/**
 * WBS 4.2 - Live Chatbot UI Component & Integration
 * Covers Test Case TC-03 ("When is the SWE488 midterm exam?" <3s DB query)
 * Covers Test Case TC-04 ("What are the course add-drop rules?" RAG Regulation query)
 * Owner: Fatih Yazıcı (20211046)
 */
import { useState } from "react";
import { apiRequest } from "../lib/api";

const SAMPLE_QUESTIONS = [
  "When is the SWE488 midterm exam?",
  "What are the course add-drop rules?",
  "What is the attendance requirement?",
];

export default function ChatbotWidget() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hello! I am your AI University Student Assistant. Ask me about exam dates (e.g. SWE488) or university regulations (e.g. add-drop rules).",
      sourceType: "SYSTEM",
      citations: [],
      responseTimeMs: null,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendQuestion = async (questionText) => {
    const trimmed = questionText.trim();
    if (!trimmed || loading) return;

    const userMsg = { role: "user", text: trimmed };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await apiRequest("/chatbot/ask/", {
        method: "POST",
        body: JSON.stringify({ question: trimmed }),
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: res.answer,
          sourceType: res.source_type,
          citations: res.citations || [],
          responseTimeMs: res.response_time_ms,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: err.message || "Unable to reach the AI Assistant service.",
          sourceType: "ERROR",
          citations: [],
          responseTimeMs: null,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendQuestion(input);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col h-[600px]">
      <div className="bg-slate-900 text-white px-5 py-4 rounded-t-xl flex items-center justify-between">
        <div>
          <h2 className="font-bold text-sm">AI Student Assistant (RAG)</h2>
          <p className="text-xs text-slate-300">
            Regulations &amp; Exam Schedule (&lt;3s NFR)
          </p>
        </div>
        <span className="h-2.5 w-2.5 rounded-full bg-emerald-400"></span>
      </div>

      {/* Quick Test Case Prompt Chips */}
      <div className="px-4 py-2.5 bg-slate-50 border-b border-slate-200 flex flex-wrap gap-1.5">
        {SAMPLE_QUESTIONS.map((q) => (
          <button
            key={q}
            type="button"
            onClick={() => sendQuestion(q)}
            className="text-xs bg-white hover:bg-red-50 text-slate-700 hover:text-red-700 border border-slate-300 px-2.5 py-1 rounded-full transition-colors"
          >
            {q}
          </button>
        ))}
      </div>

      {/* Chat Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex flex-col ${
              msg.role === "user" ? "items-end" : "items-start"
            }`}
          >
            <div
              className={`max-w-[88%] rounded-xl px-4 py-2.5 text-sm ${
                msg.role === "user"
                  ? "bg-red-700 text-white"
                  : "bg-slate-100 text-slate-800 border border-slate-200"
              }`}
            >
              <p>{msg.text}</p>

              {msg.citations && msg.citations.length > 0 && (
                <div className="mt-2 pt-2 border-t border-slate-200 text-xs text-slate-500">
                  <span className="font-semibold">Source:</span>{" "}
                  {msg.citations.join(", ")}
                </div>
              )}

              {msg.responseTimeMs !== null && msg.responseTimeMs !== undefined && (
                <div className="mt-1 text-[11px] text-emerald-700 font-medium">
                  {msg.sourceType} &bull; {msg.responseTimeMs} ms (&lt;3000ms NFR)
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="text-xs text-slate-400 italic">
            AI Assistant is searching knowledge base...
          </div>
        )}
      </div>

      {/* Chat Input Form */}
      <form
        onSubmit={handleSubmit}
        className="p-3 border-t border-slate-200 flex items-center gap-2"
      >
        <input
          type="text"
          placeholder="Ask about SWE488 exam or regulations..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 px-3.5 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-600"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-red-700 hover:bg-red-800 disabled:opacity-50 text-white font-semibold px-4 py-2 rounded-lg text-sm transition-colors"
        >
          Send
        </button>
      </form>
    </div>
  );
}
