import { Menu, CircleHelp } from "lucide-react";
export default function Header({
  title,
  status,
  onMenu,
  onHelp,
}: {
  title: string;
  status: string;
  onMenu: () => void;
  onHelp: () => void;
}) {
  return (
    <header className="header">
      <div className="header-title">
        <button
          className="icon-button mobile-menu"
          aria-label="Open navigation"
          onClick={onMenu}
        >
          <Menu size={21} />
        </button>
        <span className="breadcrumb">
          YOUR SUPPORT SPACE <span>/</span>
        </span>
        <span className="conversation-title">{title}</span>
      </div>
      <div className="header-actions">
        <span className="service-status">{status}</span>
        <button
          className="icon-button"
          onClick={onHelp}
          aria-label="About Scout"
        >
          <CircleHelp size={19} />
        </button>
      </div>
    </header>
  );
}
