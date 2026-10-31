import Link from "next/link";
import { ArrowRight, ArrowUpRight, ChevronRight } from "lucide-react";
import type { Industry } from "@/data/industries";

export default function IndustryHero({ industry }: { industry: Industry }) {
  const Icon = industry.icon;

  return (
    <section
      className="industry-hero"
      style={{ "--industry-accent": industry.accent } as React.CSSProperties}
    >
      <div className="industry-hero-grid" />

      <div className="industry-hero-inner">
        <div className="industry-breadcrumb">
          <Link href="/">Home</Link>
          <ChevronRight size={13} />
          <Link href="/solutions">Solutions</Link>
          <ChevronRight size={13} />
          <span>{industry.shortTitle}</span>
        </div>

        <div className="industry-hero-copy">
          <div className="industry-hero-label">
            <span className="industry-status-dot" />
            INDUSTRY SOLUTIONS / {industry.number}
          </div>

          <h1>{industry.title}</h1>

          <h2>{industry.subtitle}</h2>

          <p>{industry.description}</p>

          <div className="industry-hero-actions">
            <Link href="/contact" className="button-primary">
              Discuss Your Project <ArrowRight size={17} />
            </Link>

            <Link href="#solutions" className="industry-text-action">
              Explore capabilities <ArrowUpRight size={16} />
            </Link>
          </div>
        </div>

        <div className="industry-hero-visual">
          <div className="industry-visual-ring ring-a" />
          <div className="industry-visual-ring ring-b" />

          <div className="industry-visual-core">
            <Icon size={65} strokeWidth={1.2} />
            <strong>APEXIVE AI</strong>
            <span>{industry.shortTitle.toUpperCase()}</span>
          </div>

          <div className="industry-orbit-node orbit-node-a">
            <span>AI</span>
          </div>
          <div className="industry-orbit-node orbit-node-b">
            <span>DATA</span>
          </div>
          <div className="industry-orbit-node orbit-node-c">
            <span>CLOUD</span>
          </div>
        </div>
      </div>

      <div className="industry-hero-bottom">
        <span>APEXIVEAI INDUSTRY INTELLIGENCE</span>
        <span>AI · DATA · AUTOMATION · CLOUD</span>
      </div>
    </section>
  );
}