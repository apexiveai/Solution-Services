"use client";

import Link from "next/link";
import { ArrowUpRight, Globe2 } from "lucide-react";

export default function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="footer-main">
        <div className="footer-brand-column">
          <Link href="/" className="brand footer-brand">
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

          <p>
            Building intelligent enterprise solutions for a connected,
            automated and data-driven world.
          </p>

          <div className="footer-location">
            <Globe2 size={16} />
            Enterprise Technology · Global Solutions
          </div>
        </div>

        <div className="footer-column">
          <h4>Solutions</h4>
          <Link href="/solutions/telecom">Telecom</Link>
          <Link href="/solutions/transportation">Transportation</Link>
          <Link href="/solutions/manufacturing">Manufacturing</Link>
          <Link href="/solutions/public-services">Public Services</Link>
          <Link href="/solutions">All Industries</Link>
        </div>

        <div className="footer-column">
          <h4>Technologies</h4>
          <Link href="/products/ai">Artificial Intelligence</Link>
          <Link href="/products/automation">Automation</Link>
          <Link href="/products/data">Big Data & Analytics</Link>
          <Link href="/products/cloud">Cloud Solutions</Link>
        </div>

        <div className="footer-column">
          <h4>Company</h4>
          <Link href="/about">About Us</Link>
          <Link href="/professional-services">Professional Services</Link>
          <Link href="/ecosystem">Partners</Link>
          <Link href="/contact">
            Contact Us <ArrowUpRight size={13} />
          </Link>
        </div>
      </div>

      <div className="footer-bottom">
        <span>© 2026 ApexiveAI. All rights reserved.</span>
        <div>
          <Link href="/privacy">Privacy Policy</Link>
          <Link href="/terms">Terms of Use</Link>
        </div>
        <span>INTELLIGENCE IN MOTION.</span>
      </div>
    </footer>
  );
}