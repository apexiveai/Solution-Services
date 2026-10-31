import Link from "next/link";
import { ArrowRight, ArrowUpRight } from "lucide-react";
import { industries } from "@/data/industries";

export const metadata = {
  title: "Industry Solutions | ApexiveAI",
  description:
    "Explore ApexiveAI industry solutions for telecom, postal, transportation, public services, finance, energy and manufacturing.",
};

export default function SolutionsPage() {
  return (
    <>
      <section className="solutions-page-hero">
        <div className="solutions-page-hero-grid" />

        <div className="solutions-page-hero-inner">
          <div className="industry-breadcrumb">
            <Link href="/">Home</Link>
            <span>/</span>
            <span>Solutions & Services</span>
          </div>

          <span className="eyebrow">APEXIVEAI / INDUSTRY SOLUTIONS</span>

          <h1>
            Technology for
            <br />
            <span>every industry.</span>
          </h1>

          <p>
            We combine artificial intelligence, big data, cloud computing and
            enterprise platforms to help organizations modernize operations,
            connect systems and accelerate digital transformation.
          </p>

          <Link href="#industry-list" className="button-primary">
            Explore Industries <ArrowRight size={17} />
          </Link>
        </div>
      </section>

      <section className="solutions-intro">
        <div className="industry-content-container solutions-intro-grid">
          <div>
            <span className="eyebrow">INDUSTRY-FOCUSED TECHNOLOGY</span>
            <h2>
              Enterprise capabilities.
              <br />
              <span>Industry-specific solutions.</span>
            </h2>
          </div>

          <p>
            Every industry has different operational challenges. ApexiveAI
            combines a shared enterprise platform with modular industry
            applications, enabling organizations to adopt the capabilities
            they need while maintaining a consistent technology foundation.
          </p>
        </div>
      </section>

      <section className="solutions-list-section" id="industry-list">
        <div className="industry-content-container">
          <div className="industry-section-heading">
            <div>
              <span className="eyebrow">OUR INDUSTRY PORTFOLIO</span>
              <h2>
                Explore our
                <br />
                <span>industry solutions.</span>
              </h2>
            </div>

            <p>
              Discover intelligent platforms and operational capabilities
              designed for your business environment.
            </p>
          </div>

          <div className="solutions-directory-grid">
            {industries.map((industry) => {
              const Icon = industry.icon;

              return (
                <Link
                  href={`/solutions/${industry.slug}`}
                  className="solutions-directory-card"
                  key={industry.slug}
                >
                  <div className="directory-card-top">
                    <span>{industry.number} / INDUSTRY</span>
                    <div>
                      <Icon size={25} />
                    </div>
                  </div>

                  <h3>{industry.shortTitle}</h3>
                  <h4>{industry.subtitle}</h4>
                  <p>{industry.description}</p>

                  <div className="directory-card-bottom">
                    <span>Explore industry solutions</span>
                    <ArrowUpRight size={17} />
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </section>
    </>
  );
}