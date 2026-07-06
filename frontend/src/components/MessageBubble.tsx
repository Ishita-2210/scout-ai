import { useState } from "react";
import Avatar from "./Avatar";
import type { Message } from "../types/Chat";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Copy, Check } from "lucide-react";

type Props = {
  message: Message;
};

export default function MessageBubble({
  message,
}: Props) {
  const isUser = message.role === "user";
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    await navigator.clipboard.writeText(message.content);
    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 1500);
  }

  return (
    <div
      className={`message-animation flex items-start gap-4 mb-6 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      {!isUser && <Avatar role="assistant" />}

      <div
        className={`relative max-w-3xl rounded-2xl px-6 py-4 shadow-sm ${
          isUser
            ? "bg-blue-600 text-white rounded-br-md"
            : "bg-white text-slate-800 border border-slate-200 rounded-bl-md"
        }`}
      >
        {/* Header row */}
        <div className="mb-2 flex items-center justify-between">
          <span className="text-xs font-semibold uppercase tracking-wide opacity-70">
            {isUser ? "You" : "Scout AI"}
          </span>

          {/* Copy button only for assistant */}
          {!isUser && (
            <button
              onClick={handleCopy}
              className="ml-4 rounded-md p-1 hover:bg-slate-100 transition"
              title="Copy message"
            >
              {copied ? (
                <Check size={16} className="text-green-500" />
              ) : (
                <Copy size={16} className="text-slate-500" />
              )}
            </button>
          )}
        </div>

        {/* CONTENT */}
        {isUser ? (
          <div className="whitespace-pre-wrap leading-7">
            {message.content}
          </div>
        ) : (
          <div className="prose prose-slate max-w-none prose-a:text-blue-600 prose-a:underline">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        )}
      </div>

      {isUser && <Avatar role="user" />}
    </div>
  );
}