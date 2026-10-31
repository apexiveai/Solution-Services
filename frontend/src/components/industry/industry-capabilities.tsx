import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import type { Industry } from "@/data/industries";

export default function IndustryCapabilities({
  industry,
}: {
  industry: Industry;
}) {
  return (
    <>
      <section className="industry-capabilities-section" id="solutions">
        <div className="industry-content-container">
          <div className="industry-section-heading">
            <div>
              <span className="eyebrow">CORE CAPABILITIES</span>
              <h2>
                Built for complex
                <br />
                <span>industry operations.</span>
              </h2>
            </div>

            <p>
              Modular capabilities designed to work together through a unified
              enterprise platform.
            </p>
          </div>

          <div className="industry-capabilities-grid">
            {industry.capabilities.map((capability, index) => {
              const Icon = capability.icon;

              return (
                <article
                  className="industry-capability-card"
                  key={capability.title}
                >
                  <div className="industry-capability-top">
                    <span>0{index + 1}</span>
                    <div>
                      <Icon size={24} />
                    </div>
                  </div>

                  <h3>{capability.title}</h3>
                  <p>{capability.description}</p>
                  <span className="industry-card-accent" />
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section className="industry-solutions-section">
        <div className="industry-content-container">
          <div className="industry-section-heading">
            <div>
              <span className="eyebrow">SOLUTION PORTFOLIO</span>
              <h2>
                Integrated solutions.
                <br />
                <span>Measurable outcomes.</span>
              </h2>
            </div>
            <p>
              Select the capabilities that match your organization's
              operational requirements and transformation priorities.
            </p>
          </div>

          <div className="industry-solutions-grid">
            {industry.solutions.map((solution, index) => (
              <article className="industry-solution-card" key={solution.title}>
                <span className="solution-number">
                  SOLUTION / 0{index + 1}
                </span>
                <h3>{solution.title}</h3>
                <p>{solution.description}</p>
                <Link href="/contact">
                  Discuss solution <ArrowUpRight size={15} />
                </Link>
              </article>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}