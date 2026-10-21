import {
  ArrowUpRight,
  BookOpen,
  Compass,
  FileText,
  GraduationCap,
  HeartHandshake,
  House,
  MessageSquare,
  Plus,
  Scale,
  Trash2,
  X,
} from "lucide-react";
import { useEffect, useRef, useSyncExternalStore } from "react";
import type { Conversation } from "../types/Chat";
import logo from "../scout-logo.png";

const topics = [
  {
    label: "Schools & admissions",
    icon: BookOpen,
    prompt: "I need help finding a school and continuing my education.",
  },
  {
    label: "Scholarships & funding",
    icon: GraduationCap,
    prompt: "Help me find scholarships and financial support for school.",
  },
  {
    label: "Documents & certificates",
    icon: FileText,
    prompt: "I lost my school documents. How can I replace them?",
  },
  {
    label: "Housing & shelter",
    icon: House,
    prompt:
      "My family has been displaced. We need temporary housing near a school.",
  },
  {
    label: "Education rights",
    icon: Scale,
    prompt: "Help me understand my school admission rights after displacement.",
  },
  {
    label: "Learning & wellbeing",
    icon: HeartHandshake,
    prompt:
      "I am struggling to return to studying after displacement. Can you help?",
  },
];
function subscribe(listener: () => void) {
  const media = window.matchMedia("(max-width: 680px)");
  media.addEventListener("change", listener);
  return () => media.removeEventListener("change", listener);
}
const mobileSnapshot = () => window.matchMedia("(max-width: 680px)").matches;
export default function Sidebar({
  conversations,
  current,
  open,
  busy,
  onClose,
  onNew,
  onSelect,
  onDelete,
  onTopic,
  onHelp,
}: {
  conversations: Conversation[];
  current: string;
  open: boolean;
  busy: boolean;
  onClose: () => void;
  onNew: () => void;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
  onTopic: (prompt: string) => void;
  onHelp: () => void;
}) {
  const mobile = useSyncExternalStore(subscribe, mobileSnapshot);
  const sidebar = useRef<HTMLElement>(null);
  useEffect(() => {
    if (!open || !mobile) return;
    const previous = document.activeElement as HTMLElement | null;
    sidebar.current?.querySelector<HTMLButtonElement>(".close-nav")?.focus();
    return () => previous?.focus();
  }, [open, mobile]);
  return (
    <>
      {open && (
        <button
          className="sidebar-scrim"
          aria-label="Close navigation"
          onClick={onClose}
        />
      )}
      <aside
        ref={sidebar}
        className={`sidebar ${open ? "is-open" : ""}`}
        inert={mobile && !open}
        role={mobile ? "dialog" : undefined}
        aria-modal={mobile && open ? true : undefined}
        aria-label="Main navigation"
        onKeyDown={(event) => {
          if (!mobile || !open) return;
          if (event.key === "Escape") {
            onClose();
            return;
          }
          if (event.key === "Tab") {
            const buttons = [
              ...(sidebar.current?.querySelectorAll<HTMLButtonElement>(
                "button:not(:disabled)",
              ) || []),
            ];
            const first = buttons[0],
              last = buttons.at(-1);
            if (event.shiftKey && document.activeElement === first) {
              event.preventDefault();
              last?.focus();
            }
            if (!event.shiftKey && document.activeElement === last) {
              event.preventDefault();
              first?.focus();
            }
          }
        }}
      >
        <div className="brand">
          <img src={logo} alt="" />
          <div>
            scout<span>EDUCATION, CONTINUED.</span>
          </div>
          <button
            className="icon-button close-nav"
            aria-label="Close navigation"
            onClick={onClose}
          >
            <X size={20} />
          </button>
        </div>
        <button className="new-chat" disabled={busy} onClick={onNew}>
          <Plus size={18} /> New conversation <ArrowUpRight size={15} />
        </button>
        <nav aria-label="Support topics">
          <p className="nav-label">YOUR NEXT STEP</p>
          {topics.map(({ label, icon: Icon, prompt }) => (
            <button
              className="topic-link"
              key={label}
              disabled={busy}
              onClick={() => onTopic(prompt)}
            >
              <Icon size={18} />
              {label}
            </button>
          ))}
        </nav>
        <div className="recent">
          <p className="nav-label">
            CONVERSATIONS <span>{conversations.length}</span>
          </p>
          {conversations.length === 0 ? (
            <p className="recent-empty">
              A place for your questions.
              <br />
              Your conversations will appear here.
            </p>
          ) : (
            <div className="recent-list">
              {conversations.map((chat) => (
                <div
                  className={`recent-item ${current === chat.id ? "selected" : ""}`}
                  key={chat.id}
                >
                  <button
                    disabled={busy}
                    onClick={() => onSelect(chat.id)}
                    title={chat.title}
                  >
                    <MessageSquare size={15} />
                    <span>{chat.title}</span>
                  </button>
                  <button
                    className="delete-chat"
                    aria-label={`Delete conversation: ${chat.title}`}
                    disabled={busy}
                    onClick={() => onDelete(chat.id)}
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
        <div className="sidebar-bottom">
          <div className="sidebar-note">
            <Compass size={22} />
            <p>
              A little guidance.
              <br />
              <strong>A way forward.</strong>
            </p>
          </div>
          <button className="help-link" onClick={onHelp}>
            About Scout & your privacy <ArrowUpRight size={15} />
          </button>
        </div>
      </aside>
    </>
  );
}
