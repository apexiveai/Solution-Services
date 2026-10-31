"use client";

import Link from "next/link";
import { useState } from "react";
import {
  Menu,
  X,
  ChevronDown,
  RadioTower,
  Mail,
  Route,
  Landmark,
  Wallet,
  Zap,
  Factory,
  Cpu,
  BrainCircuit,
  Cloud,
  ShieldCheck,
  ArrowUpRight,
} from "lucide-react";

const industries = [
  { name: "Telecom Industry", href: "/solutions/telecom", icon: RadioTower },
  { name: "Postal Industry", href: "/solutions/postal", icon: Mail },
  {
    name: "Transportation Industry",
    href: "/solutions/transportation",
    icon: Route,
  },
  {
    name: "Public Services",
    href: "/solutions/public-services",
    icon: Landmark,
  },
  { name: "Finance Industry", href: "/solutions/finance", icon: Wallet },
  { name: "Energy Industry", href: "/solutions/energy", icon: Zap },
  {
    name: "Manufacturing Industry",
    href: "/solutions/manufacturing",
    icon: Factory,
  },
];

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
          <Link href="/products" className="nav-link">
            Products & Technologies
          </Link>

          <button
            className={`nav-link nav-trigger ${
              activeMenu === "solutions" ? "active" : ""
            }`}
            onClick={() =>
              setActiveMenu(activeMenu === "solutions" ? null : "solutions")
            }
            aria-expanded={activeMenu === "solutions"}
          >
            Solutions & Services
            <ChevronDown size={15} />
          </button>

          <Link href="/professional-services" className="nav-link">
            Professional Services
          </Link>

          <Link href="/ecosystem" className="nav-link">
            Ecosystem Partner
          </Link>

          <Link href="/insights" className="nav-link">
            Insights
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

      {activeMenu === "solutions" && (
        <div className="mega-menu">
          <div className="mega-inner">
            <div className="mega-heading">
              <span className="eyebrow">APEXIVEAI SOLUTIONS</span>
              <h2>Solutions for every industry.</h2>
              <p>
                Transform complex operations with intelligent enterprise
                platforms, industry expertise and advanced technologies.
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
                      href={industry.href}
                      className="mega-item"
                      key={industry.name}
                      onClick={closeMenus}
                    >
                      <span className="mega-icon">
                        <Icon size={19} />
                      </span>
                      <span>{industry.name}</span>
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
            </div>
          </div>
        </div>
      )}

      {mobileOpen && (
        <div className="mobile-navigation">
          <Link href="/products" onClick={closeMenus}>
            Products & Technologies
          </Link>

          <button
            onClick={() =>
              setActiveMenu(activeMenu === "mobile-solutions" ? null : "mobile-solutions")
            }
          >
            Solutions & Services <ChevronDown size={16} />
          </button>

          {activeMenu === "mobile-solutions" && (
            <div className="mobile-submenu">
              {industries.map((industry) => (
                <Link
                  key={industry.name}
                  href={industry.href}
                  onClick={closeMenus}
                >
                  {industry.name}
                </Link>
              ))}
            </div>
          )}

          <Link href="/professional-services" onClick={closeMenus}>
            Professional Services
          </Link>
          <Link href="/ecosystem" onClick={closeMenus}>
            Ecosystem Partner
          </Link>
          <Link href="/insights" onClick={closeMenus}>
            Insights
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