import {
  ArrowUpRight,
  CheckCircle2,
  Target,
} from "lucide-react";
import type { Industry } from "@/data/industries";

export default function IndustryOverview({
  industry,
}: {
  industry: Industry;
}) {
  return (
    <section className="industry-overview-section">
      <div className="industry-content-container">
        <div className="industry-overview-grid">
          <div>
            <span className="eyebrow">INDUSTRY OVERVIEW</span>
            <h2>
              A unified approach
              <br />
              to <span>{industry.shortTitle.toLowerCase()} intelligence.</span>
            </h2>
          </div>

          <div className="industry-overview-copy">
            <p>{industry.overview}</p>
            <div className="industry-overview-note">
              <Target size={19} />
              <span>
                Designed for enterprise operations, scalable deployment and
                modular industry expansion.
              </span>
            </div>
          </div>
        </div>

        <div className="industry-benefit-strip">
          {industry.benefits.map((benefit) => (
            <div className="industry-benefit" key={benefit}>
              <CheckCircle2 size={17} />
              <span>{benefit}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}