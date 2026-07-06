import { User } from "lucide-react";

type AvatarProps = {
  role: "user" | "assistant";
};

export default function Avatar({
  role,
}: AvatarProps) {
  const isUser = role === "user";

  return (
    <div
      className={`
        h-11
        w-11
        shrink-0
        overflow-hidden
        rounded-full
        shadow-sm
        ring-2
        ${
          isUser
            ? "bg-slate-900 ring-slate-300 flex items-center justify-center"
            : "ring-blue-200"
        }
      `}
    >
      {isUser ? (
        <User
          size={20}
          className="text-white"
        />
      ) : (
        <img
          src="/scout-logo.png"
          alt="Scout"
          className="h-full w-full object-cover"
        />
      )}
    </div>
  );
}