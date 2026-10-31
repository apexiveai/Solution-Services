import HeroSection from "@/components/hero-section";
import IndustrySection from "@/components/industry-section";
import Link from "next/link";
import {
  BrainCircuit,
  Workflow,
  Database,
  Cloud,
  ArrowRight,
  ShieldCheck,
} from "lucide-react";

const capabilities = [
  {
    icon: BrainCircuit,
    title: "Artificial Intelligence",
    description:
      "AI agents and intelligent systems that enhance enterprise decision-making.",
  },
  {
    icon: Workflow,
    title: "Intelligent Automation",
    description:
      "Automate complex workflows and repetitive enterprise operations.",
  },
  {
    icon: Database,
    title: "Big Data & Intelligence",
    description:
      "Transform enterprise data into actionable operational intelligence.",
  },
  {
    icon: Cloud,
    title: "Cloud & Digital Platforms",
    description:
      "Flexible cloud, on-premises and hybrid enterprise infrastructure.",
  },
];

export default function HomePage() {
  return (
    <>
      <HeroSection />

      <section className="capabilities-section">
        <div className="section-container">
          <div className="capabilities-heading">
            <span className="eyebrow">OUR TECHNOLOGY FOUNDATION</span>
            <h2>
              The intelligence behind
              <br />
              <span>enterprise transformation.</span>
            </h2>
          </div>

          <div className="capabilities-grid">
            {capabilities.map((item) => {
              const Icon = item.icon;

              return (
                <article className="capability-card" key={item.title}>
                  <div className="capability-icon">
                    <Icon size={25} strokeWidth={1.6} />
                  </div>
                  <h3>{item.title}</h3>
                  <p>{item.description}</p>
                  <span className="capability-line" />
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <IndustrySection />

      <section className="platform-section">
        <div className="platform-container">
          <div className="platform-copy">
            <span className="eyebrow eyebrow-light">
              ONE PLATFORM · MULTIPLE INDUSTRIES
            </span>

            <h2>
              Connected operations.
              <br />
              <span>Intelligent outcomes.</span>
            </h2>

            <p>
              A unified enterprise platform designed to connect business
              operations, industry applications, data and AI capabilities
              through a secure and scalable architecture.
            </p>

            <div className="platform-features">
              <span>
                <ShieldCheck size={17} /> Enterprise Security
              </span>
              <span>
                <Cloud size={17} /> Cloud & On-Premises
              </span>
              <span>
                <Workflow size={17} /> Modular Architecture
              </span>
            </div>

            <Link href="/platform" className="button-light">
              Discover the Platform <ArrowRight size={17} />
            </Link>
          </div>

          <div className="platform-visual">
            <div className="platform-core">
              <div className="platform-core-symbol">
                <BrainCircuit size={43} />
              </div>
              <strong>APEXIVE AI</strong>
              <small>ENTERPRISE CORE</small>
            </div>

            <div className="platform-node node-one">AI</div>
            <div className="platform-node node-two">DATA</div>
            <div className="platform-node node-three">CLOUD</div>
            <div className="platform-node node-four">RPA</div>
          </div>
        </div>
      </section>

      <section className="contact-section">
        <div className="contact-inner">
          <div>
            <span className="eyebrow">LET'S BUILD WHAT'S NEXT</span>
            <h2>
              Ready to transform
              <br />
              your operations?
            </h2>
            <p>
              Talk to our team about enterprise technology, intelligent
              automation and industry solutions.
            </p>
          </div>

          <Link href="/contact" className="button-primary">
            Contact ApexiveAI <ArrowRight size={17} />
          </Link>
        </div>
      </section>
    </>
  );
}