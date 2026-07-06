import {
  useEffect,
  useRef,
  useState,
} from "react";

import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import ChatInput from "../components/ChatInput";
import MessageBubble from "../components/MessageBubble";
import TypingIndicator from "../components/TypingIndicator";
import WelcomeCard from "../components/WelcomeCard";
import SuggestionGrid from "../components/SuggestionGrid";

import { sendMessage } from "../services/api";

import type { Message } from "../types/Chat";

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  async function handleSend() {
    if (!input.trim()) return;

    const prompt = input;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: prompt,
    };

    setMessages((prev) => [...prev, userMessage]);

    setInput("");

    setLoading(true);

    try {
      const response = await sendMessage({
        user_id: "test_user",
        session_id: "session_1",
        message: prompt,
      });

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: response.response,
      };

      setMessages((prev) => [
        ...prev,
        assistantMessage,
      ]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            "Unable to connect to Scout.",
        },
      ]);
    }

    setLoading(false);
  }

  function handleSuggestion(prompt: string) {
    setInput(prompt);
  }

  return (
    <div className="flex h-screen bg-slate-100">

      <Sidebar />

      <div className="flex flex-1 flex-col">

        <Header />

        <main className="flex-1 overflow-y-auto p-8">

          <div className="mx-auto max-w-5xl">

            {messages.length === 0 ? (
              <>
                <WelcomeCard userName="Ishita" />

                <SuggestionGrid
                  onSelect={handleSuggestion}
                />
              </>
            ) : (
              <>
                {messages.map((message) => (
                  <MessageBubble
                    key={message.id}
                    message={message}
                  />
                ))}

                {loading && (
                  <TypingIndicator />
                )}

                <div ref={bottomRef} />
              </>
            )}

          </div>

        </main>

        <ChatInput
          value={input}
          onChange={setInput}
          onSend={handleSend}
          loading={loading}
        />

      </div>

    </div>
  );
}