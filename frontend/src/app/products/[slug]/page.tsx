import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, ArrowRight, Check, ChevronRight } from "lucide-react";
import {
  getProduct,
  productNavigationGroups,
  products,
} from "@/data/products";

type PageProps = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return products.map(({ slug }) => ({ slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const product = getProduct(slug);

  if (!product) {
    return { title: "Product Not Found | ApexiveAI" };
  }

  return {
    title: `${product.name} | ApexiveAI`,
    description: product.summary,
  };
}

export default async function ProductPage({ params }: PageProps) {
  const { slug } = await params;
  const product = getProduct(slug);

  if (!product) {
    notFound();
  }

  const Icon = product.icon;
  const portfolioBrand = productNavigationGroups.find(
    (group) => group.family === product.family,
  )?.brand;

  return (
    <div className="product-detail-page">
      <section className="product-detail-hero">
        <div className="product-detail-hero-grid" />
        <div className="product-content-container product-detail-hero-inner">
          <nav className="product-breadcrumb" aria-label="Breadcrumb">
            <Link href="/">Home</Link><ChevronRight size={14} />
            <Link href="/products">Products</Link><ChevronRight size={14} />
            <span>{product.name}</span>
          </nav>
          <div className="product-detail-hero-layout">
            <div className="product-detail-copy">
              <span className="product-detail-category">{product.family} <span>·</span> {product.number}</span>
              {portfolioBrand && (
                <span className="product-detail-brand">{portfolioBrand}</span>
              )}
              <h1>{product.name}</h1>
              <h2>{product.tagline}</h2>
              <p>{product.summary}</p>
              <div className="product-detail-actions">
                {product.slug === "apexive-cyclone-rpa" && (
                  <>
                    <Link href="/licenses" className="button-primary">
                      Request a quote or license <ArrowRight size={17} />
                    </Link>
                    <Link href="/automation" className="product-back-link">
                      Open CoreRPA workspace <ArrowRight size={17} />
                    </Link>
                  </>
                )}
                <Link href="/contact" className="button-primary">
                  Talk to our team <ArrowRight size={17} />
                </Link>
                <Link href="/products" className="product-back-link">
                  <ArrowLeft size={15} /> All products
                </Link>
              </div>
            </div>
            <div className="product-detail-visual" aria-hidden="true">
              <div className="detail-visual-ring detail-ring-one" />
              <div className="detail-visual-ring detail-ring-two" />
              <div className="detail-visual-ring detail-ring-three" />
              <div className="detail-visual-core">
                <Icon size={48} strokeWidth={1.4} />
                <span>APEXIVE PRODUCT</span>
              </div>
              <div className="detail-visual-tag detail-tag-one">GOVERNED</div>
              <div className="detail-visual-tag detail-tag-two">CONNECTED</div>
              <div className="detail-visual-tag detail-tag-three">MODULAR</div>
            </div>
          </div>
        </div>
      </section>

      <section className="product-overview-section">
        <div className="product-content-container product-overview-grid">
          <div>
            <span className="eyebrow">PRODUCT OVERVIEW</span>
            <h2>
              Purpose-built for
              <br />
              <span>enterprise realities.</span>
            </h2>
          </div>
          <div className="product-overview-copy">
            <p>{product.overview}</p>
            <div className="product-overview-note">
              <Check size={18} />
              <span>Designed to fit into the Apexive ecosystem and your existing operating environment.</span>
            </div>
          </div>
        </div>
      </section>

      <section className="product-capabilities-section">
        <div className="product-content-container">
          <div className="product-section-heading">
            <div>
              <span className="eyebrow">CAPABILITIES</span>
              <h2>
                Built around the work
                <br />
                <span>your teams need to do.</span>
              </h2>
            </div>
            <p>Flexible capabilities can be composed around your organization, operating model and technology landscape.</p>
          </div>
          <div className="product-capabilities-grid">
            {product.capabilities.map((capability, index) => (
              <article className="product-capability-card" key={capability.title}>
                <span className="product-capability-number">{product.number}.{String(index + 1).padStart(2, "0")}</span>
                <h3>{capability.title}</h3>
                <p>{capability.description}</p>
                <span className="product-capability-accent" />
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="product-architecture-section">
        <div className="product-content-container product-architecture-layout">
          <div className="product-architecture-copy">
            <span className="eyebrow eyebrow-light">APEXIVE PLATFORM FIT</span>
            <h2>
              From enterprise foundation
              <br />
              <span>to meaningful outcomes.</span>
            </h2>
            <p>
              The product connects people, data and systems through a modular
              architecture. Start with the capabilities you need and evolve
              alongside your organization.
            </p>
            <ul className="product-outcomes-list">
              {product.outcomes.map((outcome) => (
                <li key={outcome}><Check size={17} />{outcome}</li>
              ))}
            </ul>
          </div>
          <div className="product-architecture-stack">
            {product.architecture.map((layer, index) => (
              <div className={`product-architecture-layer layer-${index + 1}`} key={layer.title}>
                <span>0{index + 1}</span>
                <div><strong>{layer.title}</strong><p>{layer.description}</p></div>
                <ChevronRight size={17} />
              </div>
            ))}
            <div className="product-architecture-caption">MODULAR BY DESIGN · ENTERPRISE READY</div>
          </div>
        </div>
      </section>

      <section className="product-detail-cta">
        <div className="product-content-container product-detail-cta-inner">
          <div>
            <span className="eyebrow">BUILT FOR YOUR NEXT MOVE</span>
            <h2>Explore what this could unlock for your organization.</h2>
            <p>Talk with ApexiveAI about fitting {product.name} into your organization&apos;s operations.</p>
          </div>
          <Link href="/contact" className="button-primary">
            Start a conversation <ArrowRight size={17} />
          </Link>
        </div>
      </section>
    </div>
  );
}
