import Link from "next/link";
import { ArrowRight, ArrowUpRight } from "lucide-react";
import { industries } from "@/data/industries";

export const metadata = {
  title: "Myanmar-Built Enterprise Solutions | ApexiveAI",
  description:
    "Explore locally developed ApexiveAI enterprise solutions for Myanmar organizations across logistics, finance, banking, government, healthcare, commerce and more.",
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

          <span className="eyebrow">APEXIVEAI / BUILT IN MYANMAR</span>

          <h1>
            Local technology.
            <br />
            <span>Solutions for Myanmar.</span>
          </h1>

          <p>
            Enterprise products and services developed by ApexiveAI in Myanmar.
            Connect existing systems and improve everyday workflows with
            locally supported solutions, including Apexive CoreRPA.
          </p>

          <Link href="#industry-list" className="button-primary">
            Explore Enterprise Solutions <ArrowRight size={17} />
          </Link>
        </div>
      </section>

      <section className="solutions-intro">
        <div className="industry-content-container solutions-intro-grid">
          <div>
            <span className="eyebrow">DESIGNED AND DEVELOPED IN MYANMAR</span>
            <h2>
              Local products.
              <br />
              <span>Configured for your operations.</span>
            </h2>
          </div>

          <p>
            ApexiveAI builds enterprise technology in Myanmar for the way local
            organizations work. Combine CoreRPA workflow automation with
            industry-focused products and services, configured for existing
            applications, approval paths and operational requirements.
          </p>
        </div>
      </section>

      <section className="solutions-list-section" id="industry-list">
        <div className="industry-content-container">
          <div className="industry-section-heading">
            <div>
              <span className="eyebrow">APEXIVEAI SOLUTION PORTFOLIO</span>
              <h2>
                Built for Myanmar.
                <br />
                <span>Explore by industry.</span>
              </h2>
            </div>

            <p>
              Explore locally developed solutions for finance, logistics,
              customer service, public services, healthcare and more.
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
                  <div className="solutions-card-visual" aria-hidden="true">
                    <span className="solutions-card-number">
                      {industry.number} / 18
                    </span>
                    <span className="solutions-card-orbit" />
                    <Icon size={58} strokeWidth={1.2} />
                    <span className="solutions-card-origin">
                      APEXIVEAI / MYANMAR
                    </span>
                  </div>

                  <div className="solutions-card-content">
                    <h3>{industry.shortTitle}</h3>
                    <h4>{industry.subtitle}</h4>
                    <p>{industry.description}</p>

                    <div className="directory-card-bottom">
                      <span>Explore {industry.shortTitle} solutions</span>
                      <ArrowUpRight size={17} />
                    </div>
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