import { ArrowDown, Compass } from "lucide-react";
export default function WelcomeCard() {
  return (
    <section className="welcome">
      <div className="eyebrow">
        <Compass size={17} /> A WAY BACK TO LEARNING
      </div>
      <h1>
        Big changes.
        <br />
        Small steps <em>forward.</em>
      </h1>
      <p>
        When life disrupts your education, you don’t have to figure everything
        out alone. Let’s find your next step, together.
      </p>
      <div className="welcome-caption">
        <span className="caption-line" />
        <span>Where would you like to begin?</span>
        <ArrowDown size={15} />
      </div>
    </section>
  );
}
