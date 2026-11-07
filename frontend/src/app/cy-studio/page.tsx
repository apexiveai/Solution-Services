import type { Metadata } from "next";
import StudioConsole from "@/components/studios/studio-console";

export const metadata: Metadata = {
  title: "CY Studio | ApexiveAI",
  description: "Design defensive CY policies and reviewed response recommendations.",
};

export default function CyStudioPage() {
  return <StudioConsole runtime="CY" />;
}
