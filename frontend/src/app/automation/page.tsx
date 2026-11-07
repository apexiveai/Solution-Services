import type { Metadata } from "next";
import AutomationConsole from "@/components/automation/automation-console";

export const metadata: Metadata = {
  title: "Apexive CoreRPA | ApexiveAI",
  description:
    "Governed workflow automation, bot orchestration and human approvals for enterprise operations.",
};

export default function AutomationPage() {
  return <AutomationConsole />;
}
