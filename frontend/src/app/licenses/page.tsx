import type { Metadata } from "next";
import CoreRpaLicensingConsole from "@/components/licensing/core-rpa-licensing-console";

export const metadata: Metadata = {
  title: "CoreRPA Licensing | ApexiveAI",
  description:
    "Request enterprise process assessments, CoreRPA quotations, software licenses and renewals.",
};

export default function LicensingPage() {
  return <CoreRpaLicensingConsole />;
}
