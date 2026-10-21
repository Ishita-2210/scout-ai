import {
  ArrowUpRight,
  BookOpen,
  FileText,
  GraduationCap,
  HeartHandshake,
  House,
  Scale,
} from "lucide-react";
const suggestions = [
  {
    title: "Get back to school",
    description: "Find a school. Understand admissions.",
    icon: BookOpen,
    category: "01 / EDUCATION",
    prompt:
      "I have been displaced and need help finding a school. Where should I start?",
  },
  {
    title: "Make learning affordable",
    description: "Explore scholarships and financial support.",
    icon: GraduationCap,
    category: "02 / FUNDING",
    prompt: "Can you help me find scholarships I may be eligible for?",
  },
  {
    title: "Replace lost documents",
    description: "Find a way forward with missing records.",
    icon: FileText,
    category: "03 / DOCUMENTS",
    prompt:
      "I lost my transfer certificate and marksheets. How can I replace them?",
  },
  {
    title: "Find a place to stay",
    description: "Look for temporary housing near schools.",
    icon: House,
    category: "04 / HOUSING",
    prompt: "I need temporary housing near a school after displacement.",
  },
  {
    title: "Understand your rights",
    description: "Get guidance on education rights and policies.",
    icon: Scale,
    category: "05 / RIGHTS",
    prompt: "What are my school admission rights if I have lost my documents?",
  },
  {
    title: "Feel ready to learn again",
    description: "Take a breath. Build a manageable study plan.",
    icon: HeartHandshake,
    category: "06 / WELLBEING",
    prompt:
      "I feel overwhelmed after displacement and need help getting back to studying.",
  },
];
export default function SuggestionGrid({
  onSelect,
  disabled,
}: {
  onSelect: (text: string) => void;
  disabled: boolean;
}) {
  return (
    <section className="suggestion-grid" aria-label="Ways Scout can help">
      {suggestions.map(
        ({ title, description, icon: Icon, category, prompt }) => (
          <button
            key={title}
            className="suggestion"
            disabled={disabled}
            onClick={() => onSelect(prompt)}
          >
            <div className="suggestion-top">
              <Icon size={23} strokeWidth={1.6} />
              <span>{category}</span>
              <ArrowUpRight size={17} />
            </div>
            <h2>{title}</h2>
            <p>{description}</p>
          </button>
        ),
      )}
    </section>
  );
}
