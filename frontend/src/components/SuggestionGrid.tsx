import {
  GraduationCap,
  School,
  FileText,
  Home,
  Scale,
  HeartHandshake,
} from "lucide-react";

type Props = {
  onSelect: (text: string) => void;
};

const suggestions = [
  {
    title: "Find Nearby Schools",
    description: "Search government and private schools nearby.",
    icon: School,
    prompt: "Find government schools near me",
  },
  {
    title: "Scholarships",
    description: "Explore scholarships you are eligible for.",
    icon: GraduationCap,
    prompt: "Find scholarships I am eligible for",
  },
  {
    title: "Lost Documents",
    description: "Recover TC, marksheets and certificates.",
    icon: FileText,
    prompt: "I lost my admission documents",
  },
  {
    title: "Housing",
    description: "Locate temporary accommodation and shelters.",
    icon: Home,
    prompt: "Help me find temporary housing",
  },
  {
    title: "Legal Help",
    description: "Know your educational rights.",
    icon: Scale,
    prompt: "I need legal assistance",
  },
  {
    title: "Counselling",
    description: "Receive emotional support resources.",
    icon: HeartHandshake,
    prompt: "I need emotional counselling",
  },
];

export default function SuggestionGrid({
  onSelect,
}: Props) {
  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {suggestions.map((item) => {
        const Icon = item.icon;

        return (
          <button
            key={item.title}
            onClick={() => onSelect(item.prompt)}
            className="rounded-2xl border border-slate-200 bg-white p-6 text-left shadow-sm transition duration-200 hover:-translate-y-1 hover:border-blue-300 hover:shadow-xl"
          >
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100">
              <Icon
                size={24}
                className="text-blue-600"
              />
            </div>

            <h3 className="text-lg font-semibold text-slate-800">
              {item.title}
            </h3>

            <p className="mt-2 text-sm leading-6 text-slate-500">
              {item.description}
            </p>
          </button>
        );
      })}
    </div>
  );
}