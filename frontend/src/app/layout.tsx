import type { Metadata } from "next";
import "./globals.css";
import SiteShell from "@/components/site-shell";

export const metadata: Metadata = {
  title: "ApexiveAI | Enterprise Operations & Intelligence",
  description:
    "AI-powered enterprise operations, intelligent automation, industry solutions and digital transformation by ApexiveAI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <SiteShell>{children}</SiteShell>
      </body>
    </html>
  );
}