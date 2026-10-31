import {
  RadioTower,
  Mail,
  Route,
  Landmark,
  Wallet,
  Zap,
  Factory,
  BrainCircuit,
  Database,
  Cloud,
  ShieldCheck,
  Workflow,
  Network,
  Activity,
  Truck,
  Map,
  Building2,
  Users,
  ClipboardCheck,
  Gauge,
  Boxes,
  Package,
  ChartNoAxesCombined,
  HeartPulse,
  Siren,
  GraduationCap,
  HardHat,
  type LucideIcon,
} from "lucide-react";

export type Industry = {
  slug: string;
  number: string;
  title: string;
  shortTitle: string;
  subtitle: string;
  description: string;
  overview: string;
  icon: LucideIcon;
  accent: string;
  capabilities: {
    title: string;
    description: string;
    icon: LucideIcon;
  }[];
  solutions: {
    title: string;
    description: string;
  }[];
  benefits: string[];
};

export const industries: Industry[] = [
  {
    slug: "telecom",
    number: "01",
    title: "Telecommunications Industry Solutions",
    shortTitle: "Telecom",
    subtitle: "Intelligent Networks. Connected Experiences.",
    description:
      "Transform telecommunications operations with AI-powered network intelligence, automation, customer experience management and enterprise data platforms.",
    overview:
      "ApexiveAI Telecom Solutions bring network operations, service management, enterprise automation and intelligent analytics together. Designed to support telecom operators and service providers through a unified operational architecture.",
    icon: RadioTower,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Network Operations Intelligence",
        description:
          "Centralized network monitoring, performance visibility and operational analytics.",
        icon: Network,
      },
      {
        title: "AI & RPA Automation",
        description:
          "Automate repetitive telecom workflows, operational processes and service tasks.",
        icon: Workflow,
      },
      {
        title: "Customer Experience Management",
        description:
          "Improve customer service workflows, case handling and service visibility.",
        icon: Users,
      },
      {
        title: "Telecom Big Data",
        description:
          "Integrate operational data for analytics, reporting and decision support.",
        icon: Database,
      },
    ],
    solutions: [
      {
        title: "Telecom RPA Platform",
        description: "Robotic process automation for telecom business operations.",
      },
      {
        title: "Network Intelligence",
        description: "Network performance monitoring and operational intelligence.",
      },
      {
        title: "Service Operations",
        description: "Customer service and enterprise service workflow management.",
      },
      {
        title: "AI Operations Center",
        description: "Unified operational insights and AI-assisted decisions.",
      },
    ],
    benefits: [
      "Centralized network and service visibility",
      "Reduced repetitive operational workloads",
      "Improved service workflow efficiency",
      "Data-driven operational decisions",
    ],
  },
  {
    slug: "postal",
    number: "02",
    title: "Postal Operations & Intelligence",
    shortTitle: "Postal",
    subtitle: "Smarter Postal Networks. Faster Deliveries.",
    description:
      "Modernize postal and courier operations with intelligent mail processing, parcel tracking, logistics data management and delivery intelligence.",
    overview:
      "A unified postal operations platform connecting postal organizations, facilities, sorting centers, delivery routes, couriers and customer services.",
    icon: Mail,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Postal Data Management",
        description: "Centralized postal organization and operational data.",
        icon: Database,
      },
      {
        title: "Parcel Tracking",
        description: "Shipment visibility and event-based tracking workflows.",
        icon: Package,
      },
      {
        title: "Delivery Operations",
        description: "Delivery planning, route assignment and courier management.",
        icon: Truck,
      },
      {
        title: "Postal Analytics",
        description: "Operational performance, delivery and service analytics.",
        icon: ChartNoAxesCombined,
      },
    ],
    solutions: [
      {
        title: "Postal Data Center",
        description: "Enterprise postal data management and integration.",
      },
      {
        title: "Smart Sorting Operations",
        description: "Mail and parcel processing workflow management.",
      },
      {
        title: "Delivery Intelligence",
        description: "Delivery planning, tracking and operational monitoring.",
      },
      {
        title: "Postal Service CRM",
        description: "Customer requests, complaints and service management.",
      },
    ],
    benefits: [
      "End-to-end parcel visibility",
      "Improved delivery coordination",
      "Centralized postal operations",
      "Better service performance analytics",
    ],
  },
  {
    slug: "transportation",
    number: "03",
    title: "Transportation Operations & Intelligence",
    shortTitle: "Transportation",
    subtitle: "Intelligent Mobility. Connected Infrastructure.",
    description:
      "Connect highway infrastructure, traffic operations, road assets, toll services and transportation intelligence through a unified platform.",
    overview:
      "ApexiveAI Transportation Solutions support highway operators, road authorities and transportation organizations with integrated infrastructure data, GIS, IoT and operational intelligence.",
    icon: Route,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Highway Operations",
        description: "Highway networks, road sections and facility management.",
        icon: Route,
      },
      {
        title: "Traffic Intelligence",
        description: "Traffic monitoring, incident workflows and service visibility.",
        icon: Activity,
      },
      {
        title: "GIS & Road Assets",
        description: "Geospatial infrastructure and road asset management.",
        icon: Map,
      },
      {
        title: "Toll & Revenue Operations",
        description: "Toll facilities, lane operations and revenue reporting.",
        icon: Wallet,
      },
    ],
    solutions: [
      {
        title: "Intelligent Highway Operations",
        description: "Road network and highway facility management.",
      },
      {
        title: "Traffic Service CRM",
        description: "Traffic-related service requests and incident management.",
      },
      {
        title: "Connected Vehicle & 5G",
        description: "Connected mobility data integration and monitoring.",
      },
      {
        title: "AI Transportation Command Center",
        description: "Unified transportation operations and decision support.",
      },
    ],
    benefits: [
      "Unified road infrastructure information",
      "Improved traffic incident visibility",
      "Better road asset lifecycle management",
      "Integrated transportation reporting",
    ],
  },
  {
    slug: "public-services",
    number: "04",
    title: "Public Services & Smart City Solutions",
    shortTitle: "Public Services",
    subtitle: "Intelligent Government. Better Public Services.",
    description:
      "Enable digital public services, smart city operations, government workflows and intelligent public infrastructure management.",
    overview:
      "An integrated digital platform for public institutions, municipalities, development zones and public service organizations.",
    icon: Landmark,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Digital Government",
        description: "Government service workflows and citizen-facing applications.",
        icon: Building2,
      },
      {
        title: "Smart City Operations",
        description: "City infrastructure monitoring and operational coordination.",
        icon: Network,
      },
      {
        title: "Public Safety",
        description: "Incident management and authorized emergency coordination.",
        icon: Siren,
      },
      {
        title: "Public Service Analytics",
        description: "Service performance, reporting and administrative intelligence.",
        icon: ChartNoAxesCombined,
      },
    ],
    solutions: [
      {
        title: "Smart Enterprise Service",
        description: "Enterprise services and government business workflows.",
      },
      {
        title: "Engineering Supervision",
        description: "Project progress, construction and quality supervision.",
      },
      {
        title: "Smart Public Service",
        description: "Digital citizen services and government affairs.",
      },
      {
        title: "Smart Campus & Elderly Care",
        description: "Campus operations and elderly care service management.",
      },
    ],
    benefits: [
      "Digitized public service workflows",
      "Better cross-department coordination",
      "Centralized city operations visibility",
      "Improved administrative reporting",
    ],
  },
  {
    slug: "finance",
    number: "05",
    title: "Financial Services & Intelligence",
    shortTitle: "Finance",
    subtitle: "Intelligent Finance. Trusted Operations.",
    description:
      "Connect financial workflows, enterprise data, operational automation and business intelligence in a secure digital environment.",
    overview:
      "ApexiveAI Financial Solutions provide modular operational capabilities for financial institutions and enterprise finance departments.",
    icon: Wallet,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Financial Data Management",
        description: "Structured financial information and reporting workflows.",
        icon: Database,
      },
      {
        title: "Process Automation",
        description: "Automated document, approval and reconciliation workflows.",
        icon: Workflow,
      },
      {
        title: "Risk & Compliance Workflows",
        description: "Configurable control, review and audit processes.",
        icon: ShieldCheck,
      },
      {
        title: "Financial Analytics",
        description: "Operational and management reporting.",
        icon: ChartNoAxesCombined,
      },
    ],
    solutions: [
      {
        title: "Financial Operations",
        description: "Finance process and workflow management.",
      },
      {
        title: "Intelligent Reconciliation",
        description: "Data-assisted reconciliation and exception handling.",
      },
      {
        title: "Document Intelligence",
        description: "Document extraction and processing automation.",
      },
      {
        title: "Financial Command Center",
        description: "Unified financial operational insights.",
      },
    ],
    benefits: [
      "Improved financial workflow consistency",
      "Reduced manual processing",
      "Centralized audit visibility",
      "Faster operational reporting",
    ],
  },
  {
    slug: "energy",
    number: "06",
    title: "Energy Operations & Intelligence",
    shortTitle: "Energy",
    subtitle: "Smarter Energy. Resilient Infrastructure.",
    description:
      "Connect energy infrastructure, operational data, asset monitoring and intelligent analytics for modern energy organizations.",
    overview:
      "An integrated energy operations platform for utilities and energy organizations, with infrastructure visibility, operational analytics and secure integration.",
    icon: Zap,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Energy Asset Management",
        description: "Asset inventory, lifecycle and maintenance records.",
        icon: Gauge,
      },
      {
        title: "Infrastructure Monitoring",
        description: "Read-only operational telemetry and event visibility.",
        icon: Activity,
      },
      {
        title: "Energy Data Analytics",
        description: "Energy consumption and operational data analysis.",
        icon: ChartNoAxesCombined,
      },
      {
        title: "Field Operations",
        description: "Field service coordination and work order management.",
        icon: Workflow,
      },
    ],
    solutions: [
      {
        title: "Energy Data Platform",
        description: "Energy information integration and governance.",
      },
      {
        title: "Smart Utility Operations",
        description: "Utility asset and operational management.",
      },
      {
        title: "Predictive Maintenance",
        description: "Data-driven equipment maintenance insights.",
      },
      {
        title: "Energy Command Center",
        description: "Centralized monitoring and operational reporting.",
      },
    ],
    benefits: [
      "Improved asset visibility",
      "Centralized energy data",
      "Better maintenance planning",
      "More informed operational decisions",
    ],
  },
  {
    slug: "manufacturing",
    number: "07",
    title: "Manufacturing & Industry 4.0 Solutions",
    shortTitle: "Manufacturing",
    subtitle: "Smart Factories. Intelligent Production.",
    description:
      "Transform industrial operations with Industry 4.0 data management, industrial IoT, smart factory capabilities and AI-powered analytics.",
    overview:
      "ApexiveAI Manufacturing Solutions connect production, industrial equipment, quality, supply chain, warehouse and enterprise systems through an integrated data and operations platform.",
    icon: Factory,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Industrial Data Management",
        description: "Integrate factory data and establish governed industrial datasets.",
        icon: Database,
      },
      {
        title: "Smart Factory Operations",
        description: "Factory, production line and operational visibility.",
        icon: Factory,
      },
      {
        title: "Industrial IoT",
        description: "Connect authorized sensors, gateways and industrial data sources.",
        icon: Network,
      },
      {
        title: "Predictive Maintenance",
        description: "Analyze equipment telemetry to support maintenance planning.",
        icon: Gauge,
      },
      {
        title: "Quality Management",
        description: "Quality inspection, nonconformance and corrective action workflows.",
        icon: ClipboardCheck,
      },
      {
        title: "Supply Chain & Warehouse",
        description: "Inventory, procurement, material movement and warehouse visibility.",
        icon: Boxes,
      },
    ],
    solutions: [
      {
        title: "Industry 4.0 Data Management",
        description: "Industrial data integration, governance and analytics.",
      },
      {
        title: "Production Intelligence",
        description: "Production planning, output tracking and operational reporting.",
      },
      {
        title: "Industrial IoT Platform",
        description: "Sensor, PLC and SCADA data integration through secure gateways.",
      },
      {
        title: "AI Manufacturing Command Center",
        description: "Unified factory performance, quality and equipment insights.",
      },
    ],
    benefits: [
      "Connected industrial data",
      "Improved production visibility",
      "Data-driven maintenance planning",
      "Integrated quality and inventory operations",
    ],
  },
];

export function getIndustry(slug: string) {
  return industries.find((industry) => industry.slug === slug);
}