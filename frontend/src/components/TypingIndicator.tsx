export default function TypingIndicator() {
  return (
    <div className="flex items-start gap-3 mb-6">

      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-blue-600 to-cyan-500 shadow-sm">
        🤖
      </div>

      <div className="rounded-2xl rounded-bl-md border border-slate-200 bg-white px-5 py-4 shadow-sm">

        <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-500">
          Scout AI
        </p>

        <div className="flex items-center gap-2">

          <span className="h-2.5 w-2.5 animate-bounce rounded-full bg-blue-500" />

          <span
            className="h-2.5 w-2.5 animate-bounce rounded-full bg-blue-500"
            style={{ animationDelay: "0.15s" }}
          />

          <span
            className="h-2.5 w-2.5 animate-bounce rounded-full bg-blue-500"
            style={{ animationDelay: "0.3s" }}
          />

        </div>

      </div>

    </div>
  );
}