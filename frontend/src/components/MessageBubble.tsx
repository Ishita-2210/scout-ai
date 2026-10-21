import { useState } from "react";
import { Check, Copy, ExternalLink, AlertCircle } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Avatar from "./Avatar";
import type { AssistantResult, Message } from "../types/Chat";

function label(value: string) {
  return value.replaceAll("_", " ").replace(/^./, (c) => c.toUpperCase());
}
function safeUrl(value: string) {
  return /^https?:\/\//i.test(value) ? value : undefined;
}

function StructuredValue({
  value,
  depth = 0,
}: {
  value: unknown;
  depth?: number;
}) {
  if (value == null || value === "" || depth > 5) return null;
  if (typeof value === "string") {
    const url = safeUrl(value);
    return url ? (
      <a href={url} target="_blank" rel="noopener noreferrer">
        Visit website <ExternalLink size={12} />
      </a>
    ) : (
      <span>{value}</span>
    );
  }
  if (typeof value === "boolean") return <span>{value ? "Yes" : "No"}</span>;
  if (typeof value === "number") return <span>{value}</span>;
  if (Array.isArray(value))
    return value.length ? (
      <ul className="structured-list">
        {value.map((item, i) => (
          <li key={i}>
            <StructuredValue value={item} depth={depth + 1} />
          </li>
        ))}
      </ul>
    ) : null;
  if (typeof value === "object")
    return (
      <dl className="structured-fields">
        {Object.entries(value)
          .filter(
            ([key, v]) =>
              key !== "query" &&
              v != null &&
              v !== "" &&
              (!Array.isArray(v) || v.length > 0),
          )
          .map(([key, v]) => (
            <div key={key}>
              <dt>{label(key)}</dt>
              <dd>
                <StructuredValue value={v} depth={depth + 1} />
              </dd>
            </div>
          ))}
      </dl>
    );
  return null;
}
function Markdown({ text }: { text: string }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        a: ({ href, children }) =>
          safeUrl(href || "") ? (
            <a href={href} target="_blank" rel="noopener noreferrer">
              {children}
            </a>
          ) : (
            <span>{children}</span>
          ),
      }}
    >
      {text}
    </ReactMarkdown>
  );
}
export default function MessageBubble({ message }: { message: Message }) {
  const [copyStatus, setCopyStatus] = useState("");
  const isUser = message.role === "user";
  const result: AssistantResult =
    typeof message.content === "string"
      ? { text: message.content }
      : message.content;
  async function copy() {
    try {
      await navigator.clipboard.writeText(
        result.text +
          (result.sections?.length
            ? "\n\n" +
              JSON.stringify(
                result.sections.map((s) => s.data),
                null,
                2,
              )
            : ""),
      );
      setCopyStatus("Copied");
    } catch {
      setCopyStatus("Could not copy. Select the text to copy it.");
    }
  }
  return (
    <article
      className={`message ${isUser ? "user-message" : "assistant-message"}`}
      aria-label={isUser ? "Your message" : "Scout response"}
    >
      <div className="message-heading">
        <Avatar role={message.role} />
        <span>
          {isUser ? "YOU" : "SCOUT"}
          <small>
            {isUser ? "Your question" : "A little clarity for your next step"}
          </small>
        </span>
        {!isUser && (
          <button
            className="copy-button"
            onClick={copy}
            aria-label="Copy response"
          >
            {copyStatus === "Copied" ? <Check size={15} /> : <Copy size={15} />}
            <span>{copyStatus === "Copied" ? "Copied" : "Copy"}</span>
          </button>
        )}
      </div>
      <div className="message-body">
        {isUser ? (
          <p className="user-text">{result.text}</p>
        ) : (
          <>
            <div className="markdown">
              <Markdown text={result.text} />
            </div>
            {result.sections?.map((section, i) => {
              const hasDetails = Object.entries(section.data).some(
                ([key, value]) =>
                  key !== "query" &&
                  (Array.isArray(value)
                    ? value.length > 0
                    : value != null && value !== ""),
              );
              return hasDetails ? (
                <details
                  className="result-details"
                  key={`${section.domain}-${i}`}
                >
                  <summary>{section.title} · details & next steps</summary>
                  <StructuredValue value={section.data} />
                </details>
              ) : null;
            })}
            {!!result.warnings?.length && (
              <div className="result-warnings">
                {result.warnings.map((warning, i) => (
                  <p key={i}>
                    <AlertCircle size={15} />
                    {warning}
                  </p>
                ))}
              </div>
            )}
            {!!result.sources?.length && (
              <div className="sources">
                <h3>Sources to explore</h3>
                {result.sources
                  .filter((s) => safeUrl(s.url))
                  .map((source, i) => (
                    <a
                      href={source.url}
                      key={`${source.url}-${i}`}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <span>{i + 1}</span>
                      {source.title}
                      <ExternalLink size={13} />
                    </a>
                  ))}
              </div>
            )}
            {!!result.references?.length && (
              <p className="reference-note">
                Reference material supplied to Scout:{" "}
                {result.references.join("; ")}. These documents may be outdated.
              </p>
            )}
            {copyStatus && (
              <span role="status" className="copy-status">
                {copyStatus}
              </span>
            )}
          </>
        )}
      </div>
    </article>
  );
}
