import type { Metadata } from "next";
import StudioConsole from "@/components/studios/studio-console";

export const metadata: Metadata = {
  title: "AIS Studio | ApexiveAI",
  description: "Design governed AIS workflows for the licensed Apexive CoreRPA orchestrator.",
};

export default function AisStudioPage() {
  return <StudioConsole runtime="AIS" />;
}
