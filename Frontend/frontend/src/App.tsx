import { useState, useRef } from "react";
import ReactMarkdown from "react-markdown";

interface Message {
  role: "user" | "agent";
  text: string;
}

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;

    setMessages((prev) => [...prev, { role: "user", text: userMessage }]);
    setInput("");

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }

    // Add an empty agent message to stream into
    setMessages((prev) => [...prev, { role: "agent", text: "" }]);

    const response = await fetch("http://127.0.0.1:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: userMessage }),
    });

    const reader = response.body!.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const text = decoder.decode(value);
      setMessages((prev) => {
        const updated = [...prev];
        const last = updated[updated.length - 1];
        if (last.role === "agent") {
          updated[updated.length - 1] = {
            ...last,
            text: last.text + text,
          };
        }
        return updated;
      });
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    const el = textareaRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = el.scrollHeight + "px";
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-[#1a1a1a] text-white flex flex-col">

      {messages.length === 0 ? (
        <div className="flex flex-col items-center justify-center flex-1">
          <h1 className="text-4xl mb-6">AI Research Agent</h1>

          <div className="flex flex-col w-150 border p-3 rounded-2xl shadow-[0_0_8px_rgba(255,255,255,0.3)]">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={handleInput}
              onKeyDown={handleKeyDown}
              rows={1}
              placeholder="Ask Anything..."
              className="w-full min-h-10 max-h-50 bg-transparent resize-none overflow-hidden outline-none"
            />

            <button
              onClick={sendMessage}
              disabled={!input.trim()}
              className="mt-2 self-end bg-gray-600 px-4 py-1 rounded-xl hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Ask
            </button>
          </div>
        </div>
      ) : (
        <div className="flex flex-col flex-1">

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6">
            <div className="max-w-3xl mx-auto space-y-4">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`max-w-[70%] w-fit p-3 rounded-xl ${
                  msg.role === "user"
                    ? "bg-gray-600 ml-auto"
                    : "bg-gray-800"
                }`}
              >
                <ReactMarkdown>{msg.text}</ReactMarkdown>
              </div>
            ))}
            </div>
          </div>

          {/* Bottom Input */}
          <div className="border-t border-gray-700 p-4">
            <div className="max-w-3xl mx-auto flex gap-2">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={handleInput}
                onKeyDown={handleKeyDown}
                rows={1}
                placeholder="Ask Anything..."
                className="flex-1 min-h-10 max-h-50 bg-transparent resize-none overflow-hidden outline-none border border-gray-700 rounded-xl p-2"
              />

              <button
                onClick={sendMessage}
                disabled={!input.trim()}
                className="bg-gray-600 px-4 rounded-xl hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed self-end"
              >
                Ask
              </button>
            </div>
          </div>

        </div>
      )}
    </div>
  );
}

export default App;