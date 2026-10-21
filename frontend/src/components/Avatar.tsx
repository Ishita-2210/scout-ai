import logo from "../scout-logo.png";
export default function Avatar({ role }: { role: "user" | "assistant" }) {
  return role === "assistant" ? (
    <img className="avatar" src={logo} alt="" />
  ) : (
    <span className="avatar user-avatar">You</span>
  );
}
