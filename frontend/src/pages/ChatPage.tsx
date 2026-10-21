import { useEffect, useRef, useState } from "react";
import { AlertCircle, ArrowRight, Compass, RefreshCw } from "lucide-react";
import AboutDialog from "../components/AboutDialog";
import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import ChatInput from "../components/ChatInput";
import MessageBubble from "../components/MessageBubble";
import TypingIndicator from "../components/TypingIndicator";
import WelcomeCard from "../components/WelcomeCard";
import SuggestionGrid from "../components/SuggestionGrid";
import {
  ApiError,
  deleteConversation,
  getConversations,
  getMessages,
  initializeSession,
  sendMessage,
} from "../services/api";
import type { Conversation, Message, ServiceStatus } from "../types/Chat";

function savedId() {
  try {
    return sessionStorage.getItem("scout-conversation") || crypto.randomUUID();
  } catch {
    return crypto.randomUUID();
  }
}
export default function ChatPage() {
  const [current, setCurrent] = useState(savedId);
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [status, setStatus] = useState<ServiceStatus | null>(null);
  const [initialized, setInitialized] = useState(false);
  const [startupAttempt, setStartupAttempt] = useState(0);
  const [error, setError] = useState("");
  const [failedPrompt, setFailedPrompt] = useState("");
  const [retryAt, setRetryAt] = useState(0);
  const [now, setNow] = useState(() => Date.now());
  const [navOpen, setNavOpen] = useState(false);
  const [historyError, setHistoryError] = useState("");
  const pending = useRef(false);
  const controller = useRef<AbortController | null>(null);
  const historyController = useRef<AbortController | null>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const bottom = useRef<HTMLDivElement>(null);
  const scrollArea = useRef<HTMLElement>(null);
  const dialog = useRef<HTMLDialogElement>(null);
  const retrySeconds = Math.max(0, Math.ceil((retryAt - now) / 1000));

  useEffect(() => {
    let live = true;
    const abort = new AbortController();
    async function load() {
      try {
        const state = await initializeSession();
        if (!live) return;
        const chats = await getConversations();
        const id = savedId();
        const restored = chats.some((c) => c.id === id)
          ? await getMessages(id, abort.signal)
          : [];
        if (live) {
          setStatus(state);
          setConversations(chats);
          setCurrent(id);
          setMessages(restored);
          setInitialized(true);
          setError("");
        }
      } catch (err) {
        if (live)
          setError(
            err instanceof Error ? err.message : "Scout could not be reached.",
          );
      }
    }
    void load();
    return () => {
      live = false;
      abort.abort();
    };
  }, [startupAttempt]);
  useEffect(() => {
    try {
      sessionStorage.setItem("scout-conversation", current);
    } catch {
      /* Storage may be disabled. Server history still works. */
    }
  }, [current]);
  useEffect(() => {
    if (messages.length === 0 && !loading) {
      scrollArea.current?.scrollTo({ top: 0 });
      return;
    }
    bottom.current?.scrollIntoView({
      behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
        ? "instant"
        : "smooth",
      block: "end",
    });
  }, [messages, loading]);
  useEffect(() => {
    if (!retryAt) return;
    const timer = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, [retryAt]);
  useEffect(
    () => () => {
      controller.current?.abort();
      historyController.current?.abort();
    },
    [],
  );

  function selectPrompt(prompt: string) {
    setInput(prompt);
    setNavOpen(false);
    window.setTimeout(() => inputRef.current?.focus(), 0);
  }
  function newChat() {
    if (pending.current) return;
    historyController.current?.abort();
    setCurrent(crypto.randomUUID());
    setMessages([]);
    setInput("");
    setError("");
    setFailedPrompt("");
    setNavOpen(false);
    setHistoryLoading(false);
    window.setTimeout(() => inputRef.current?.focus(), 0);
  }
  async function selectChat(id: string) {
    if (pending.current) return;
    historyController.current?.abort();
    const abort = new AbortController();
    historyController.current = abort;
    setHistoryLoading(true);
    setError("");
    setFailedPrompt("");
    setNavOpen(false);
    try {
      const rows = await getMessages(id, abort.signal);
      if (!abort.signal.aborted) {
        setMessages(rows);
        setCurrent(id);
        setInput("");
      }
    } catch (err) {
      if (!abort.signal.aborted)
        setError(
          err instanceof Error
            ? err.message
            : "Conversation could not be loaded.",
        );
    } finally {
      if (!abort.signal.aborted) setHistoryLoading(false);
    }
  }
  async function removeChat(id: string) {
    if (pending.current || historyLoading) return;
    try {
      await deleteConversation(id);
      setConversations((prev) => prev.filter((c) => c.id !== id));
      if (id === current) newChat();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Conversation could not be deleted.",
      );
    }
  }
  async function refreshHistory() {
    try {
      setConversations(await getConversations());
      setHistoryError("");
    } catch {
      setHistoryError(
        "Your answer is saved, but the conversation list could not refresh.",
      );
    }
  }
  async function send(prompt = input, retry = false) {
    prompt = prompt.trim();
    if (
      !prompt ||
      pending.current ||
      historyLoading ||
      !initialized ||
      !status?.ready ||
      retrySeconds > 0
    )
      return;
    pending.current = true;
    setLoading(true);
    setError("");
    setFailedPrompt("");
    setInput("");
    if (!retry)
      setMessages((prev) => [
        ...prev,
        { id: crypto.randomUUID(), role: "user", content: prompt },
      ]);
    const abort = new AbortController();
    controller.current = abort;
    const timeout = window.setTimeout(() => abort.abort("timeout"), 125000);
    try {
      const result = await sendMessage(
        {
          session_id: current,
          request_id: crypto.randomUUID(),
          message: prompt,
        },
        abort.signal,
      );
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: result.response,
        },
      ]);
      setRetryAt(0);
      await refreshHistory();
    } catch (err) {
      const stopped = abort.signal.aborted;
      setError(
        stopped
          ? "The request stopped. Check saved conversation history before trying again."
          : err instanceof Error
            ? err.message
            : "Scout could not complete your request.",
      );
      setFailedPrompt(prompt);
      if (err instanceof ApiError && err.retryAfter) {
        setNow(Date.now());
        setRetryAt(Date.now() + err.retryAfter * 1000);
      }
    } finally {
      window.clearTimeout(timeout);
      pending.current = false;
      controller.current = null;
      setLoading(false);
    }
  }
  const currentTitle =
    conversations.find((c) => c.id === current)?.title ||
    (messages.length ? "Your conversation" : "A fresh start");
  const statusText = !initialized
    ? "Connecting…"
    : status?.ready
      ? "Ready for your question"
      : "Setup needed";
  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">
        Skip to conversation
      </a>
      <Sidebar
        conversations={conversations}
        current={current}
        open={navOpen}
        busy={loading || historyLoading || !initialized}
        onClose={() => setNavOpen(false)}
        onNew={newChat}
        onSelect={(id) => void selectChat(id)}
        onDelete={(id) => void removeChat(id)}
        onTopic={selectPrompt}
        onHelp={() => dialog.current?.showModal()}
      />
      <div className="workspace">
        <Header
          title={currentTitle}
          status={statusText}
          onMenu={() => setNavOpen(true)}
          onHelp={() => dialog.current?.showModal()}
        />
        <main
          ref={scrollArea}
          id="main-content"
          className="main-content"
          tabIndex={-1}
          aria-busy={historyLoading}
        >
          <div
            className={
              messages.length ? "conversation-content" : "welcome-content"
            }
          >
            {!status?.ready && initialized && (
              <div className="notice">
                <AlertCircle size={18} />
                <p>
                  Scout needs a quick setup before it can answer. Ask the
                  administrator to configure the AI service.
                </p>
              </div>
            )}
            {historyLoading ? (
              <div className="history-loading" role="status">
                Loading your conversation…
              </div>
            ) : messages.length === 0 ? (
              <>
                <WelcomeCard />
                <SuggestionGrid
                  onSelect={selectPrompt}
                  disabled={loading || !initialized}
                />
                <div className="start-note">
                  <Compass size={18} />
                  <p>
                    You can start with just a question.
                    <br />
                    <span>No need to have it all figured out.</span>
                  </p>
                  <ArrowRight size={18} />
                </div>
              </>
            ) : (
              <div className="messages" aria-label="Conversation messages">
                {messages.map((message) => (
                  <MessageBubble key={message.id} message={message} />
                ))}
              </div>
            )}
            {loading && <TypingIndicator />}
            {error && (
              <div className="error-notice" role="alert">
                <AlertCircle size={19} />
                <div>
                  <p>{error}</p>
                  {failedPrompt && initialized && (
                    <button
                      disabled={loading || retrySeconds > 0}
                      onClick={() => void send(failedPrompt, true)}
                    >
                      <RefreshCw size={14} />
                      {retrySeconds
                        ? `Try again in ${retrySeconds}s`
                        : "Try this question again"}
                    </button>
                  )}
                  {!initialized && (
                    <button
                      onClick={() => {
                        setError("");
                        setStartupAttempt((n) => n + 1);
                      }}
                    >
                      Reconnect
                    </button>
                  )}
                </div>
              </div>
            )}
            {historyError && (
              <div className="notice">
                <p>{historyError}</p>
                <button onClick={() => void refreshHistory()}>
                  Refresh list
                </button>
              </div>
            )}
            <div ref={bottom} />
          </div>
        </main>
        <ChatInput
          ref={inputRef}
          value={input}
          onChange={setInput}
          onSend={() => void send()}
          onStop={() => controller.current?.abort()}
          loading={loading}
          disabled={
            !initialized || !status?.ready || historyLoading || retrySeconds > 0
          }
        />
      </div>
      <AboutDialog
        dialogRef={dialog}
        busy={loading || historyLoading}
        onDeleted={() => {
          setConversations([]);
          newChat();
        }}
        onError={setError}
      />
    </div>
  );
}
