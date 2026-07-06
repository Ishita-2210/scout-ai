import {
  Plus,
  MessageSquare,
  School,
  GraduationCap,
  FileText,
  Home,
  Scale,
  HeartHandshake,
} from "lucide-react";

const quickActions = [
  {
    icon: School,
    label: "Schools",
  },
  {
    icon: GraduationCap,
    label: "Scholarships",
  },
  {
    icon: FileText,
    label: "Documents",
  },
  {
    icon: Home,
    label: "Housing",
  },
  {
    icon: Scale,
    label: "Legal Help",
  },
  {
    icon: HeartHandshake,
    label: "Counselling",
  },
];

export default function Sidebar() {
  return (
    <aside className="w-72 bg-slate-900 text-white flex flex-col">

      {/* Top */}

      <div className="p-6">

        <button
          className="
            w-full
            flex
            items-center
            justify-center
            gap-3
            rounded-xl
            bg-blue-600
            py-3
            font-medium
            shadow-lg
            transition
            hover:bg-blue-700
          "
        >
          <Plus size={18} />
          New Chat
        </button>

      </div>

      {/* Recent Chats */}

      <div className="px-6">

        <p className="mb-3 text-xs uppercase tracking-widest text-slate-400">
          Recent Chats
        </p>

        <div className="space-y-2">

          <button className="flex w-full items-center gap-3 rounded-lg px-3 py-3 hover:bg-slate-800 transition">
            <MessageSquare size={18} />
            Lost Transfer Certificate
          </button>

          <button className="flex w-full items-center gap-3 rounded-lg px-3 py-3 hover:bg-slate-800 transition">
            <MessageSquare size={18} />
            Scholarship Eligibility
          </button>

          <button className="flex w-full items-center gap-3 rounded-lg px-3 py-3 hover:bg-slate-800 transition">
            <MessageSquare size={18} />
            Nearby Schools
          </button>

        </div>

      </div>

      {/* Quick Actions */}

      <div className="mt-8 px-6">

        <p className="mb-3 text-xs uppercase tracking-widest text-slate-400">
          Quick Access
        </p>

        <div className="space-y-2">

          {quickActions.map((item) => {

            const Icon = item.icon;

            return (

              <button
                key={item.label}
                className="
                  flex
                  w-full
                  items-center
                  gap-3
                  rounded-lg
                  px-3
                  py-3
                  transition
                  hover:bg-slate-800
                "
              >
                <Icon size={18} />

                {item.label}

              </button>

            );

          })}

        </div>

      </div>

      {/* Bottom */}

      <div className="mt-auto border-t border-slate-700 p-6">

        <div className="flex items-center gap-3">

          <div className="flex h-11 w-11 items-center justify-center rounded-full bg-blue-600 text-lg font-semibold">
            I
          </div>

          <div>

            <p className="font-medium">
              Ishita
            </p>

            <p className="text-sm text-slate-400">
              Student
            </p>

          </div>

        </div>

      </div>

    </aside>
  );
}