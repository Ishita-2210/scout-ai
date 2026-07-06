import { SendHorizontal } from "lucide-react";

type ChatInputProps = {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  loading: boolean;
};

export default function ChatInput({
  value,
  onChange,
  onSend,
  loading,
}: ChatInputProps) {
  return (
    <div className="border-t border-slate-200 bg-white px-8 py-6">

      <div className="mx-auto flex max-w-5xl items-center gap-4">

        <input
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !loading) {
              onSend();
            }
          }}
          placeholder="Ask Scout anything..."
          className="
            flex-1
            rounded-2xl
            border
            border-slate-300
            bg-white
            px-6
            py-4
            text-slate-700
            outline-none
            transition
            focus:border-blue-600
            focus:ring-4
            focus:ring-blue-100
          "
        />

        <button
          onClick={onSend}
          disabled={loading}
          className="
            flex
            h-14
            w-14
            items-center
            justify-center
            rounded-2xl
            bg-blue-600
            text-white
            shadow-md
            transition
            hover:bg-blue-700
            disabled:cursor-not-allowed
            disabled:opacity-50
          "
        >
          {loading ? (
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent" />
          ) : (
            <SendHorizontal size={22} />
          )}
        </button>

      </div>

    </div>
  );
}