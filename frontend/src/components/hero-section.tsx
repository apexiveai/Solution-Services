import Link from "next/link";
import {
  ArrowRight,
  ArrowUpRight,
  BrainCircuit,
  Network,
  Workflow,
} from "lucide-react";

export default function HeroSection() {
  return (
    <section className="hero-section">
      <div className="hero-background-grid" />

      <div className="hero-container">
        <div className="hero-content">
          <div className="hero-badge">
            <span className="status-dot" />
            INTELLIGENT ENTERPRISE TECHNOLOGY
          </div>

          <h1>
            Intelligence that
            <br />
            moves business
            <br />
            <span>forward.</span>
          </h1>

          <p className="hero-description">
            Empowering enterprises and industries through artificial
            intelligence, intelligent automation, big data and next-generation
            digital platforms.
          </p>

          <div className="hero-actions">
            <Link href="/solutions" className="button-primary">
              Explore Solutions <ArrowRight size={17} />
            </Link>

            <Link href="/contact" className="button-secondary">
              Talk to Our Team <ArrowUpRight size={16} />
            </Link>
          </div>

          <div className="hero-trust">
            <span>ENGINEERED FOR ENTERPRISE</span>
            <span className="trust-divider" />
            <span>BUILT FOR THE FUTURE</span>
          </div>
        </div>

        <div className="hero-visual">
          <div className="visual-orbit orbit-one" />
          <div className="visual-orbit orbit-two" />

          <div className="visual-center">
            <div className="visual-center-inner">
              <BrainCircuit size={48} strokeWidth={1.3} />
              <strong>APEXIVE AI</strong>
              <span>INTELLIGENCE CORE</span>
            </div>
          </div>

          <div className="floating-card floating-card-one">
            <span className="floating-icon blue">
              <Network size={19} />
            </span>
            <div>
              <strong>Connected Enterprise</strong>
              <small>Unified Operations</small>
            </div>
          </div>

          <div className="floating-card floating-card-two">
            <span className="floating-icon purple">
              <BrainCircuit size={19} />
            </span>
            <div>
              <strong>AI Intelligence</strong>
              <small>Decision Support</small>
            </div>
          </div>

          <div className="floating-card floating-card-three">
            <span className="floating-icon green">
              <Workflow size={19} />
            </span>
            <div>
              <strong>Automation</strong>
              <small>Intelligent Workflows</small>
            </div>
          </div>
        </div>
      </div>

      <div className="hero-bottom-line">
        <span>01 / ENTERPRISE INTELLIGENCE</span>
        <span>AI · DATA · AUTOMATION · CLOUD</span>
      </div>
    </section>
  );
}