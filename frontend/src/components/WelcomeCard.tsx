type WelcomeCardProps = {
  userName?: string;
};

export default function WelcomeCard({
  userName = "there",
}: WelcomeCardProps) {
  return (
    <div className="mb-14 text-center">

      <div className="mb-6 flex justify-center">

        <div className="flex h-24 w-24 items-center justify-center rounded-3xl bg-gradient-to-br from-blue-600 to-cyan-500 text-5xl shadow-xl">
          🤖
        </div>

      </div>

      <h1 className="text-5xl font-bold tracking-tight text-slate-900">
        Welcome, {userName}
      </h1>

      <p className="mt-5 text-xl text-slate-600">
        I'm Scout, your AI Disaster Education Assistant.
      </p>

      <p className="mx-auto mt-3 max-w-3xl text-slate-500 leading-8">
        I can help you find schools, scholarships,
        replace lost documents, understand legal
        rights, locate temporary housing, and
        provide counselling resources during
        emergencies.
      </p>

      <div className="mt-10 flex flex-wrap justify-center gap-3">

        <span className="rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700">
          🏫 Schools
        </span>

        <span className="rounded-full bg-green-100 px-4 py-2 text-sm font-medium text-green-700">
          🎓 Scholarships
        </span>

        <span className="rounded-full bg-orange-100 px-4 py-2 text-sm font-medium text-orange-700">
          📄 Documents
        </span>

        <span className="rounded-full bg-purple-100 px-4 py-2 text-sm font-medium text-purple-700">
          ⚖️ Legal Help
        </span>

        <span className="rounded-full bg-pink-100 px-4 py-2 text-sm font-medium text-pink-700">
          ❤️ Counselling
        </span>

      </div>

    </div>
  );
}