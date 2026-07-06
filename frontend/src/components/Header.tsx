import { Bell, Settings } from "lucide-react";

export default function Header() {
  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 shadow-sm">

      <div className="flex items-center gap-4">

        <div className="h-12 w-12 overflow-hidden rounded-xl shadow-md">
          <img
            src="/scout-logo.png"
            alt="Scout"
            className="h-full w-full object-cover"
          />
        </div>

        <div>

          <h1 className="text-xl font-bold text-slate-900">
            Scout AI
          </h1>

          <p className="text-sm text-slate-500">
            Disaster Education Assistant
          </p>

        </div>

      </div>

      <div className="flex items-center gap-6">

        <div className="flex items-center gap-2">

          <div className="h-2.5 w-2.5 rounded-full bg-green-500 animate-pulse" />

          <span className="text-sm text-slate-600">
            Online
          </span>

        </div>

        <button className="rounded-lg p-2 transition hover:bg-slate-100">
          <Bell size={20} />
        </button>

        <button className="rounded-lg p-2 transition hover:bg-slate-100">
          <Settings size={20} />
        </button>

      </div>

    </header>
  );
}