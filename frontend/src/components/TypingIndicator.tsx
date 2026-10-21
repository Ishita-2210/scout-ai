import { LoaderCircle } from "lucide-react";
export default function TypingIndicator() {
  return (
    <div className="thinking" role="status">
      <LoaderCircle size={17} className="spinner" />
      <span>Scout is working through your question…</span>
    </div>
  );
}
