"use client";

import type { ReactNode } from "react";
import { usePathname } from "next/navigation";
import SiteFooter from "@/components/site-footer";
import SiteHeader from "@/components/site-header";
import CycloneRpaHeader from "@/components/cyclone-rpa/cyclone-rpa-header";

const cycloneRpaRoutes = [
  "/cyclone-rpa",
  "/automation",
  "/ais-studio",
  "/cy-studio",
  "/licenses",
];

export default function SiteShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const isCycloneRpa = cycloneRpaRoutes.some(
    (route) => pathname === route || pathname.startsWith(`${route}/`),
  );

  if (isCycloneRpa) {
    return (
      <>
        <CycloneRpaHeader />
        {children}
      </>
    );
  }

  return (
    <>
      <SiteHeader />
      <main>{children}</main>
      <SiteFooter />
    </>
  );
}
