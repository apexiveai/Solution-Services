import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { industries, getIndustry } from "@/data/industries";
import IndustryHero from "@/components/industry/industry-hero";
import IndustryOverview from "@/components/industry/industry-overview";
import IndustryCapabilities from "@/components/industry/industry-capabilities";
import IndustryCTA from "@/components/industry/industry-cta";

type PageProps = {
  params: Promise<{ industry: string }>;
};

export function generateStaticParams() {
  return industries.map((industry) => ({
    industry: industry.slug,
  }));
}

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { industry: slug } = await params;
  const industry = getIndustry(slug);

  if (!industry) {
    return {
      title: "Industry Not Found | ApexiveAI",
    };
  }

  return {
    title: `${industry.shortTitle} Solutions | ApexiveAI`,
    description: industry.description,
  };
}

export default async function IndustryPage({ params }: PageProps) {
  const { industry: slug } = await params;
  const industry = getIndustry(slug);

  if (!industry) {
    notFound();
  }

  return (
    <>
      <IndustryHero industry={industry} />
      <IndustryOverview industry={industry} />
      <IndustryCapabilities industry={industry} />
      <IndustryCTA industry={industry} />
    </>
  );
}