import type { Metadata } from "next";
import Link from "next/link";
import { ArrowDown, ArrowRight, BrainCircuit, Database, Network } from "lucide-react";
import ProductDirectory from "@/components/products/product-directory";

export const metadata: Metadata = {
  title: "Myanmar-Built Products | ApexiveAI",
  description:
    "Explore locally developed ApexiveAI products for Myanmar organizations, including Apexive CoreRPA, enterprise AI, data intelligence and connected operations.",
};

const portfolioPillars = [
  { title: "Developed in Myanmar", description: "A locally built technology portfolio shaped around Myanmar organizations.", icon: BrainCircuit },
  { title: "Fits local workflows", description: "Flexible capabilities designed to work with the processes teams already use.", icon: Database },
  { title: "Connects existing systems", description: "Bring AI, data and operations together without replacing every business tool.", icon: Network },
];

export default function ProductsPage() {
  return (
    <>
      <section className="products-hero">
        <div className="products-hero-grid" />
        <div className="products-hero-inner">
          <div className="industry-breadcrumb">
            <Link href="/">Home</Link>
            <span>/</span>
            <span>Products & Technologies</span>
          </div>
          <div className="products-hero-layout">
            <div className="products-hero-copy">
              <span className="eyebrow">APEXIVEAI / MYANMAR-BUILT PRODUCTS</span>
              <h1>
                Technology built here.
                <br />
                <span>Ready for local work.</span>
              </h1>
              <p>
                Explore ApexiveAI products developed in Myanmar for local
                organizations — from enterprise AI and data platforms to
                network operations and Apexive CoreRPA.
              </p>
              <Link href="#product-directory" className="button-primary">
                Explore our products <ArrowRight size={17} />
              </Link>
            </div>

            <div className="products-hero-visual" role="img" aria-label="ApexiveAI product portfolio">
              <div className="product-orbit product-orbit-one" />
              <div className="product-orbit product-orbit-two" />
              <div className="product-orbit product-orbit-three" />
              <div className="products-core">
                <BrainCircuit size={35} />
                <strong>APEXIVE</strong>
                <span>MYANMAR-BUILT TECHNOLOGY</span>
              </div>
              <div className="products-orbit-node product-node-one">AI</div>
              <div className="products-orbit-node product-node-two">DATA</div>
              <div className="products-orbit-node product-node-three">OPS</div>
            </div>
          </div>
          <a className="products-scroll-cue" href="#portfolio-pillars">
            <span>EXPLORE THE PLATFORM</span>
            <ArrowDown size={15} />
          </a>
        </div>
      </section>

      <section className="product-pillars-section" id="portfolio-pillars">
        <div className="product-content-container">
          <div className="product-pillars-heading">
            <span className="eyebrow">A LOCAL TECHNOLOGY PORTFOLIO</span>
            <h2>
              Designed to work
              <br />
              <span>better together.</span>
            </h2>
          </div>
          <div className="product-pillars-grid">
            {portfolioPillars.map((pillar, index) => {
              const Icon = pillar.icon;

              return (
                <article className="product-pillar-card" key={pillar.title}>
                  <span className="product-pillar-number">0{index + 1}</span>
                  <div className="product-pillar-icon"><Icon size={23} /></div>
                  <h3>{pillar.title}</h3>
                  <p>{pillar.description}</p>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <ProductDirectory />
    </>
  );
}
