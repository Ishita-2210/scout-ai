import { ArrowUp, Square } from "lucide-react";
import { forwardRef } from "react";
const ChatInput = forwardRef<
  HTMLTextAreaElement,
  {
    value: string;
    onChange: (value: string) => void;
    onSend: () => void;
    onStop: () => void;
    loading: boolean;
    disabled: boolean;
  }
>(function ChatInput(
  { value, onChange, onSend, onStop, loading, disabled },
  ref,
) {
  return (
    <div className="composer-wrap">
      <form
        className="composer"
        onSubmit={(event) => {
          event.preventDefault();
          onSend();
        }}
      >
        <label htmlFor="message" className="sr-only">
          Your message to Scout
        </label>
        <textarea
          ref={ref}
          id="message"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          maxLength={4000}
          rows={2}
          disabled={disabled || loading}
          placeholder="Tell Scout what you need help with…"
          onKeyDown={(event) => {
            if (
              event.key === "Enter" &&
              !event.shiftKey &&
              !event.nativeEvent.isComposing
            ) {
              event.preventDefault();
              if (!loading) onSend();
            }
          }}
        />
        <div className="composer-bottom">
          <span>
            {value.length > 3500
              ? `${value.length.toLocaleString()} / 4,000`
              : "Your location and grade can help Scout guide you."}
          </span>
          {loading ? (
            <button
              className="send-button stop-button"
              type="button"
              aria-label="Stop request"
              onClick={onStop}
            >
              <Square size={15} />
            </button>
          ) : (
            <button
              className="send-button"
              type="submit"
              aria-label="Send message"
              disabled={disabled || !value.trim()}
            >
              <ArrowUp size={20} />
            </button>
          )}
        </div>
      </form>
      <p className="composer-disclaimer">
        Scout can make mistakes. Confirm important details with official
        sources. <span>Enter to send · Shift + Enter for a new line</span>
      </p>
    </div>
  );
});
export default ChatInput;
