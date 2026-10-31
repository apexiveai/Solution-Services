import Link from "next/link";
import { ArrowRight, ShieldCheck, Cloud, Workflow } from "lucide-react";
import type { Industry } from "@/data/industries";

export default function IndustryCTA({
  industry,
}: {
  industry: Industry;
}) {
  return (
    <>
      <section className="industry-architecture-section">
        <div className="industry-content-container">
          <div className="industry-section-heading">
            <div>
              <span className="eyebrow">PLATFORM ARCHITECTURE</span>
              <h2>
                One platform.
                <br />
                <span>Flexible deployment.</span>
              </h2>
            </div>

            <p>
              Deploy the {industry.shortTitle} solution portfolio using a
              deployment model that matches your organization's infrastructure
              and security requirements.
            </p>
          </div>

          <div className="architecture-stack">
            <div className="architecture-layer architecture-top">
              <strong>INDUSTRY APPLICATIONS</strong>
              <span>{industry.solutions.map((item) => item.title).join(" · ")}</span>
            </div>

            <div className="architecture-connector" />

            <div className="architecture-layer architecture-middle">
              <strong>APEXIVEAI SHARED PLATFORM</strong>
              <span>
                Identity · Tenant Management · Workflow · Licensing · Audit
              </span>
            </div>

            <div className="architecture-connector" />

            <div className="architecture-layer architecture-bottom">
              <strong>INTELLIGENCE & INTEGRATION</strong>
              <span>AI · Big Data · APIs · IoT · Analytics</span>
            </div>

            <div className="architecture-deployment">
              <span><Cloud size={17} /> CLOUD</span>
              <span><ShieldCheck size={17} /> ON-PREMISES</span>
              <span><Workflow size={17} /> HYBRID</span>
            </div>
          </div>
        </div>
      </section>

      <section className="industry-cta-section">
        <div className="industry-cta-inner">
          <div>
            <span className="eyebrow eyebrow-light">
              LET'S TRANSFORM YOUR OPERATIONS
            </span>
            <h2>
              Build the future of
              <br />
              {industry.shortTitle.toLowerCase()} with ApexiveAI.
            </h2>
            <p>
              Discuss your requirements with our enterprise solutions team.
            </p>
          </div>

          <Link href="/contact" className="button-light">
            Request a Consultation <ArrowRight size={17} />
          </Link>
        </div>
      </section>
    </>
  );
}