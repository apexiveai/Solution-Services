import type { Metadata } from "next";
import AisWorkflowStudio from "@/components/studios/ais-workflow-studio";

export const metadata: Metadata = {
  title: "AIS Studio | ApexiveAI",
  description: "Design governed AIS workflows for the licensed Apexive CoreRPA orchestrator.",
};

export default function AisStudioPage() {
  return <AisWorkflowStudio />;
}
