"use client";

import Link from "next/link";
import { useState } from "react";
import {
  Menu,
  X,
  ChevronDown,
  Cpu,
  BrainCircuit,
  Cloud,
  ShieldCheck,
  ArrowUpRight,
  Activity,
  Workflow,
  Container,
} from "lucide-react";
import {
  productNavigationGroups,
  products,
} from "@/data/products";
import { industries } from "@/data/industries";

const technologies = [
  {
    title: "Artificial Intelligence",
    description: "AI agents, intelligent automation and decision support.",
    icon: BrainCircuit,
  },
  {
    title: "Big Data & Analytics",
    description: "Enterprise data platforms and business intelligence.",
    icon: Cpu,
  },
  {
    title: "Cloud & Infrastructure",
    description: "Cloud-native, on-premises and hybrid deployments.",
    icon: Cloud,
  },
  {
    title: "Cybersecurity",
    description: "Identity, access control and enterprise security.",
    icon: ShieldCheck,
  },
];

const professionalServices = [
  {
    title: "Consultation Services",
    description: "Strategy, architecture design and expert advisory services.",
    href: "/professional-services#consultation-services",
    icon: BrainCircuit,
  },
  {
    title: "Operation Services",
    description: "Managed operations, monitoring and system maintenance.",
    href: "/professional-services#operation-services",
    icon: Activity,
  },
  {
    title: "Integration Services",
    description: "Seamless system integration and workflow automation.",
    href: "/professional-services#integration-services",
    icon: Workflow,
  },
  {
    title: "Kubernetes-Related Services",
    description: "Cluster deployment, orchestration and cloud-native management.",
    href: "/professional-services#kubernetes-services",
    icon: Container,
  },
];

export default function SiteHeader() {
  const [activeMenu, setActiveMenu] = useState<string | null>(null);
  const [mobileOpen, setMobileOpen] = useState(false);

  function closeMenus() {
    setActiveMenu(null);
    setMobileOpen(false);
  }

  return (
    <header className="site-header">
      <div className="header-main">
        <Link href="/" className="brand" onClick={closeMenus}>
          <span className="brand-symbol">
            <span />
            <span />
            <span />
          </span>

          <span className="brand-copy">
            <strong>APEXIVE<span>AI</span></strong>
            <small>INTELLIGENCE IN MOTION</small>
          </span>
        </Link>

        <nav className="desktop-nav" aria-label="Main navigation">
          <button
            className={`nav-link nav-trigger ${
              activeMenu === "products" ? "active" : ""
            }`}
            onClick={() =>
              setActiveMenu(activeMenu === "products" ? null : "products")
            }
            aria-expanded={activeMenu === "products"}
            aria-controls="products-mega-menu"
          >
            Products
            <ChevronDown size={15} />
          </button>

          <button
            className={`nav-link nav-trigger ${
              activeMenu === "solutions" ? "active" : ""
            }`}
            onClick={() =>
              setActiveMenu(activeMenu === "solutions" ? null : "solutions")
            }
            aria-expanded={activeMenu === "solutions"}
            aria-controls="solutions-mega-menu"
          >
            Enterprise Solutions
            <ChevronDown size={15} />
          </button>

          <Link href="/professional-services" className="nav-link">
            Professional Services
          </Link>

          <Link href="/ecosystem" className="nav-link">
            Alliance & Partners
          </Link>

          <Link href="/insights" className="nav-link">
            Knowledge Hub
          </Link>

          <Link href="/about" className="nav-link">
            About ApexiveAI
          </Link>
        </nav>

        <div className="header-actions">
          <Link href="/login" className="login-link">
            Log In <ArrowUpRight size={15} />
          </Link>

          <Link href="/contact" className="header-contact">
            Contact Us
          </Link>

          <button
            className="mobile-menu-button"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle navigation"
          >
            {mobileOpen ? <X /> : <Menu />}
          </button>
        </div>
      </div>

      {activeMenu === "products" && (
        <div className="mega-menu products-mega-menu" id="products-mega-menu">
          <div className="products-mega-inner">
            <div className="products-mega-heading">
              <div>
                <span className="eyebrow">APEXIVE / PRODUCTS FOR MYANMAR</span>
                <h2>Technology built for local operations.</h2>
                <p>
                  Explore locally developed products for AI, data, networks,
                  operations and enterprise automation.
                </p>
              </div>
              <Link
                href="/products"
                className="products-mega-explore"
                onClick={closeMenus}
              >
                Explore all products <ArrowUpRight size={15} />
              </Link>
            </div>

            <div className="products-mega-groups">
              {productNavigationGroups.map((group) => (
                <section className="products-mega-group" key={group.title}>
                  <div className="products-mega-group-heading">
                    <span>{group.title}</span>
                    <strong>{group.brand}</strong>
                    <p>{group.description}</p>
                  </div>
                  <div className="products-mega-grid">
                    {products
                      .filter((product) => product.family === group.family)
                      .map((product) => {
                        const Icon = product.icon;

                        return (
                          <Link
                            href={`/products/${product.slug}`}
                            className="products-mega-item"
                            key={product.slug}
                            onClick={closeMenus}
                          >
                            <span className="products-mega-icon">
                              <Icon size={17} />
                            </span>
                            <span>
                              <strong>{product.name}</strong>
                              <small>{product.tagline}</small>
                            </span>
                            <ArrowUpRight
                              className="products-mega-arrow"
                              size={14}
                            />
                          </Link>
                        );
                      })}
                  </div>
                </section>
              ))}
            </div>
            <section className="products-mega-group">
              <div className="products-mega-group-heading">
                <span>CoreRPA Studios</span>
                <strong>Apexive Intelligence & Defense</strong>
                <p>Separate, governed studios built on versioned runtime contracts.</p>
              </div>
              <div className="products-mega-grid">
                <Link
                  href="/ais-studio"
                  className="products-mega-item"
                  onClick={closeMenus}
                >
                  <span className="products-mega-icon"><BrainCircuit size={17} /></span>
                  <span><strong>AIS Studio</strong><small>AI workflows and model tasks</small></span>
                  <ArrowUpRight className="products-mega-arrow" size={14} />
                </Link>
                <Link
                  href="/cy-studio"
                  className="products-mega-item"
                  onClick={closeMenus}
                >
                  <span className="products-mega-icon"><ShieldCheck size={17} /></span>
                  <span><strong>CY Studio</strong><small>Defensive alerts and response policies</small></span>
                  <ArrowUpRight className="products-mega-arrow" size={14} />
                </Link>
              </div>
            </section>
          </div>
        </div>
      )}

      {activeMenu === "solutions" && (
        <div className="mega-menu solutions-mega-menu" id="solutions-mega-menu">
          <div className="mega-inner">
            <div className="mega-heading">
              <span className="eyebrow">APEXIVEAI / MYANMAR-BUILT SOLUTIONS</span>
              <h2>Local technology for local operations.</h2>
              <p>
                Explore solutions developed by ApexiveAI in Myanmar and
                configured around your organization&apos;s workflows and systems.
              </p>

              <Link
                href="/solutions"
                className="mega-explore"
                onClick={closeMenus}
              >
                Explore all solutions <ArrowUpRight size={16} />
              </Link>
            </div>

            <div className="mega-content">
              <div className="mega-label">INDUSTRY SOLUTIONS</div>

              <div className="mega-industry-grid">
                {industries.map((industry) => {
                  const Icon = industry.icon;

                  return (
                    <Link
                      href={`/solutions/${industry.slug}`}
                      className="mega-item"
                      key={industry.slug}
                      onClick={closeMenus}
                    >
                      <span className="mega-icon">
                        <Icon size={19} />
                      </span>
                      <span>{industry.shortTitle}</span>
                      <ArrowUpRight className="mega-arrow" size={14} />
                    </Link>
                  );
                })}
              </div>

              <div className="mega-label technology-label">
                TECHNOLOGY & CAPABILITIES
              </div>

              <div className="technology-grid">
                {technologies.map((technology) => {
                  const Icon = technology.icon;

                  return (
                    <div className="technology-item" key={technology.title}>
                      <Icon size={19} />
                      <div>
                        <strong>{technology.title}</strong>
                        <p>{technology.description}</p>
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="mega-label professional-services-label">
                PROFESSIONAL SERVICES
              </div>

              <div className="professional-services-menu-grid">
                {professionalServices.map((service) => {
                  const Icon = service.icon;

                  return (
                    <Link
                      href={service.href}
                      className="professional-services-menu-item"
                      key={service.title}
                      onClick={closeMenus}
                    >
                      <span className="professional-services-menu-icon">
                        <Icon size={18} />
                      </span>
                      <span className="professional-services-menu-copy">
                        <strong>{service.title}</strong>
                        <small>{service.description}</small>
                      </span>
                      <ArrowUpRight
                        className="professional-services-menu-arrow"
                        size={14}
                      />
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {mobileOpen && (
        <div className="mobile-navigation">
          <button
            aria-expanded={activeMenu === "mobile-products"}
            onClick={() =>
              setActiveMenu(
                activeMenu === "mobile-products" ? null : "mobile-products",
              )
            }
          >
            Products <ChevronDown size={16} />
          </button>

          {activeMenu === "mobile-products" && (
            <div className="mobile-submenu mobile-product-submenu">
              {productNavigationGroups.map((group) => (
                <div className="mobile-product-group" key={group.title}>
                  <strong>{group.title}</strong>
                  <small>{group.brand}</small>
                  {products
                    .filter((product) => product.family === group.family)
                    .map((product) => (
                      <Link
                        key={product.slug}
                        href={`/products/${product.slug}`}
                        onClick={closeMenus}
                      >
                        {product.name}
                        <ArrowUpRight size={13} />
                      </Link>
                    ))}
                </div>
              ))}
              <Link href="/products" onClick={closeMenus}>
                Explore all products
              </Link>
            </div>
          )}

          <button
            onClick={() =>
              setActiveMenu(activeMenu === "mobile-solutions" ? null : "mobile-solutions")
            }
          >
            Enterprise Solutions <ChevronDown size={16} />
          </button>

          {activeMenu === "mobile-solutions" && (
            <div className="mobile-submenu">
              {industries.map((industry) => (
                <Link
                  key={industry.slug}
                  href={`/solutions/${industry.slug}`}
                  onClick={closeMenus}
                >
                  {industry.shortTitle}
                </Link>
              ))}
              <div className="mobile-service-menu">
                <strong>Professional Services</strong>
                {professionalServices.map((service) => (
                  <Link
                    key={service.title}
                    href={service.href}
                    onClick={closeMenus}
                  >
                    <span>
                      <b>{service.title}</b>
                      <small>{service.description}</small>
                    </span>
                    <ArrowUpRight size={14} />
                  </Link>
                ))}
              </div>
            </div>
          )}

          <Link href="/professional-services" onClick={closeMenus}>
            Professional Services
          </Link>
          <Link href="/ecosystem" onClick={closeMenus}>
            Alliance & Partners
          </Link>
          <Link href="/insights" onClick={closeMenus}>
            Knowledge Hub
          </Link>
          <Link href="/about" onClick={closeMenus}>
            About ApexiveAI
          </Link>
          <Link href="/login" onClick={closeMenus}>
            Log In
          </Link>
        </div>
      )}
    </header>
  );
}