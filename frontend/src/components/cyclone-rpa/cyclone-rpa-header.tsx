"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ArrowUpRight, Bot, Menu, X } from "lucide-react";
import { useState } from "react";
import styles from "./cyclone-rpa.module.css";

const navigation = [
  { label: "Overview", href: "/cyclone-rpa", exact: true },
  { label: "Capabilities", href: "/cyclone-rpa#capabilities" },
  { label: "Architecture", href: "/cyclone-rpa#architecture" },
  { label: "Roadmap", href: "/cyclone-rpa#roadmap" },
  { label: "Studio", href: "/ais-studio" },
  { label: "Orchestrator", href: "/automation" },
  { label: "License Center", href: "/licenses" },
];

export default function CycloneRpaHeader() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  function closeMenu() {
    setMobileOpen(false);
  }

  return (
    <header className={styles.header}>
      <div className={styles.headerInner}>
        <Link href="/cyclone-rpa" className={styles.brand} onClick={closeMenu}>
          <span className={styles.brandMark}><Bot size={20} /></span>
          <span className={styles.brandText}>
            <strong>Cyclone <span>RPA</span></strong>
            <small>APEXIVEAI AUTOMATION</small>
          </span>
        </Link>

        <nav className={styles.desktopNav} aria-label="Cyclone RPA navigation">
          {navigation.map((item) => {
            const active = item.exact
              ? pathname === item.href
              : pathname === "/cyclone-rpa" && item.href.includes("#")
                ? false
                : pathname === item.href;
            return (
              <Link
                key={item.label}
                href={item.href}
                className={active ? styles.activeNavLink : ""}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className={styles.headerActions}>
          <Link className={styles.workspaceLink} href="/automation">
            Open workspace <ArrowUpRight size={14} />
          </Link>
          <button
            type="button"
            className={styles.mobileMenuButton}
            aria-label={mobileOpen ? "Close navigation" : "Open navigation"}
            aria-expanded={mobileOpen}
            onClick={() => setMobileOpen((open) => !open)}
          >
            {mobileOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {mobileOpen && (
        <nav className={styles.mobileNav} aria-label="Cyclone RPA mobile navigation">
          {navigation.map((item) => (
            <Link href={item.href} key={item.label} onClick={closeMenu}>
              {item.label}{!item.exact && item.href.startsWith("/") && !item.href.includes("#") && <ArrowUpRight size={14} />}
            </Link>
          ))}
        </nav>
      )}
    </header>
  );
}
