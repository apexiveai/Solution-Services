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
  {
    slug: "logistics",
    number: "08",
    title: "Logistics Operations Solutions",
    shortTitle: "Logistics",
    subtitle: "Move Goods. Connect Every Handoff.",
    description:
      "Coordinate orders, warehouses, transport partners and delivery updates with automation built around the realities of Myanmar logistics operations.",
    overview:
      "Apexive CoreRPA helps logistics teams connect order and shipment information across existing business systems, spreadsheets, email and partner channels. Automate repeatable coordination while keeping exceptions visible to the people who need to resolve them.",
    icon: Truck,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Order & Shipment Processing",
        description:
          "Capture shipment requests and synchronize order details across approved systems.",
        icon: Package,
      },
      {
        title: "Warehouse Coordination",
        description:
          "Automate inventory updates, picking lists and dispatch handoffs.",
        icon: Boxes,
      },
      {
        title: "Delivery Status Management",
        description:
          "Collect status updates from internal teams and delivery partners.",
        icon: Route,
      },
      {
        title: "Exception & Document Handling",
        description:
          "Route missing documents, delivery exceptions and approvals for review.",
        icon: ClipboardCheck,
      },
    ],
    solutions: [
      {
        title: "Shipment Data Automation",
        description:
          "Move shipment information between order, warehouse and tracking systems.",
      },
      {
        title: "Dispatch Workflow",
        description:
          "Coordinate dispatch schedules, delivery documents and handoffs.",
      },
      {
        title: "Proof-of-Delivery Processing",
        description:
          "Collect delivery records and flag incomplete or inconsistent submissions.",
      },
      {
        title: "Logistics Operations Dashboard",
        description:
          "Review shipment progress, pending work and exceptions in one place.",
      },
    ],
    benefits: [
      "Less repeated data entry",
      "Clearer shipment and delivery status",
      "Faster handling of operational exceptions",
      "A practical path to connect existing tools",
    ],
  },
  {
    slug: "banking",
    number: "09",
    title: "Banking Operations Solutions",
    shortTitle: "Banking",
    subtitle: "Reliable Workflows. Accountable Operations.",
    description:
      "Automate repeatable banking back-office work, document handling and service requests with review points for sensitive actions.",
    overview:
      "CoreRPA supports banking teams with controlled workflows that connect existing systems and organize operational work. Human approval remains part of the process wherever policy, risk or customer impact requires it.",
    icon: Landmark,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Customer Onboarding Support",
        description:
          "Organize submitted information and route incomplete applications for follow-up.",
        icon: Users,
      },
      {
        title: "Transaction Operations",
        description:
          "Automate authorized data preparation, validation and work allocation.",
        icon: Workflow,
      },
      {
        title: "Account Service Requests",
        description:
          "Track requests, approvals and completion status across service teams.",
        icon: ClipboardCheck,
      },
      {
        title: "Audit-Ready Process Records",
        description:
          "Keep workflow status, approvals and exception histories traceable.",
        icon: ShieldCheck,
      },
    ],
    solutions: [
      {
        title: "Banking Document Intake",
        description:
          "Classify and route forms and supporting documents for staff review.",
      },
      {
        title: "Back-Office Workflow Automation",
        description:
          "Coordinate recurring operations across approved banking applications.",
      },
      {
        title: "Service Request Orchestration",
        description:
          "Assign, track and escalate customer and internal service requests.",
      },
      {
        title: "Operations & Exception Reporting",
        description:
          "Monitor outstanding tasks, handoffs and items needing attention.",
      },
    ],
    benefits: [
      "More consistent operational processing",
      "Visible approval and exception handling",
      "Reduced manual copying between systems",
      "Human review for controlled decisions",
    ],
  },
  {
    slug: "ecommerce",
    number: "10",
    title: "eCommerce Operations Solutions",
    shortTitle: "eCommerce",
    subtitle: "Connect Orders to Fulfillment.",
    description:
      "Bring online orders, inventory, customer support and delivery coordination into connected workflows for local commerce teams.",
    overview:
      "CoreRPA helps merchants and online sellers manage repetitive work across storefronts, marketplaces, inventory tools and delivery partners. Teams can start with the systems they already use and expand automation as operations grow.",
    icon: Package,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Order Management",
        description:
          "Collect order details and coordinate confirmation, packing and fulfillment.",
        icon: Workflow,
      },
      {
        title: "Inventory Synchronization",
        description:
          "Update stock records across connected sales and inventory channels.",
        icon: Boxes,
      },
      {
        title: "Customer Support Workflows",
        description:
          "Route order questions, returns and delivery issues to the right team.",
        icon: Users,
      },
      {
        title: "Sales & Settlement Reconciliation",
        description:
          "Compare order and settlement records and highlight mismatches.",
        icon: ChartNoAxesCombined,
      },
    ],
    solutions: [
      {
        title: "Order-to-Dispatch Automation",
        description:
          "Coordinate new orders, stock checks, packing and dispatch tasks.",
      },
      {
        title: "Marketplace Data Sync",
        description:
          "Transfer approved product, order and fulfillment information.",
      },
      {
        title: "Returns & Refund Workflow",
        description:
          "Track return requests, review steps and refund status.",
      },
      {
        title: "Commerce Operations Reporting",
        description:
          "Bring order volumes, fulfillment progress and exceptions together.",
      },
    ],
    benefits: [
      "Fewer missed order handoffs",
      "More consistent stock updates",
      "Quicker routing of customer issues",
      "Clearer order and settlement visibility",
    ],
  },
  {
    slug: "healthcare",
    number: "11",
    title: "Healthcare & Hospital Operations",
    shortTitle: "Healthcare",
    subtitle: "Connected Administration. More Time for Care.",
    description:
      "Reduce administrative friction across appointments, records and supplies while keeping clinical decisions with qualified professionals.",
    overview:
      "Apexive CoreRPA supports healthcare providers with administrative workflow automation, connecting existing systems and reducing repetitive coordination. It is designed to assist staff rather than make clinical decisions or replace professional judgment.",
    icon: HeartPulse,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Patient Administration",
        description:
          "Coordinate registration, appointment and administrative follow-up tasks.",
        icon: Users,
      },
      {
        title: "Document & Records Routing",
        description:
          "Organize forms and route records through authorized staff workflows.",
        icon: ClipboardCheck,
      },
      {
        title: "Billing Administration",
        description:
          "Prepare billing information and flag discrepancies for staff review.",
        icon: Wallet,
      },
      {
        title: "Supply & Facility Coordination",
        description:
          "Track supply requests, inventory updates and maintenance tasks.",
        icon: Boxes,
      },
    ],
    solutions: [
      {
        title: "Appointment Administration",
        description:
          "Coordinate appointment reminders, confirmations and rescheduling tasks.",
      },
      {
        title: "Patient Document Workflow",
        description:
          "Route submitted administrative documents to authorized teams.",
      },
      {
        title: "Billing & Claims Preparation",
        description:
          "Gather supporting information and track review status.",
      },
      {
        title: "Hospital Operations Coordination",
        description:
          "Manage non-clinical requests, handoffs and administrative reporting.",
      },
    ],
    benefits: [
      "Less time spent on repetitive administration",
      "Clearer patient-service handoffs",
      "More organized billing and document workflows",
      "Clinical decisions remain with care professionals",
    ],
  },
  {
    slug: "human-resources",
    number: "12",
    title: "Human Resources Solutions",
    shortTitle: "Human Resources",
    subtitle: "Simplify the Employee Journey.",
    description:
      "Connect recruitment, onboarding, employee requests and payroll preparation with workflows that fit your organization's processes.",
    overview:
      "CoreRPA helps HR teams manage recurring administrative work across hiring, employee records, leave and payroll preparation. Access and approvals can follow organizational roles, with staff review for sensitive employment decisions.",
    icon: Users,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Recruitment Coordination",
        description:
          "Track applications, interview schedules and candidate follow-ups.",
        icon: ClipboardCheck,
      },
      {
        title: "Employee Onboarding",
        description:
          "Coordinate forms, account requests and onboarding task completion.",
        icon: Workflow,
      },
      {
        title: "Employee Service Requests",
        description:
          "Route leave, document and policy requests with status visibility.",
        icon: Users,
      },
      {
        title: "Payroll Data Preparation",
        description:
          "Collect and validate payroll inputs for authorized staff review.",
        icon: Database,
      },
    ],
    solutions: [
      {
        title: "Recruitment Workflow",
        description:
          "Coordinate candidate information, interviews and hiring approvals.",
      },
      {
        title: "Joiner-Mover-Leaver Automation",
        description:
          "Manage employee changes and related access or equipment requests.",
      },
      {
        title: "Leave & Attendance Administration",
        description:
          "Synchronize requests and records across approved HR tools.",
      },
      {
        title: "HR Service Desk",
        description:
          "Organize employee questions, document requests and follow-up tasks.",
      },
    ],
    benefits: [
      "More consistent employee administration",
      "Faster coordination between HR and other teams",
      "Improved visibility into pending requests",
      "Reviewable handling of sensitive employee data",
    ],
  },
  {
    slug: "supply-chain",
    number: "13",
    title: "Supply Chain Management Solutions",
    shortTitle: "Supply Chain",
    subtitle: "Connect Suppliers, Inventory and Delivery.",
    description:
      "Improve coordination across procurement, suppliers, inventory and distribution with practical automation for multi-step operations.",
    overview:
      "CoreRPA connects the routine information flows that keep supply chains moving. Automate purchase and inventory updates across current tools, and route shortages, delayed deliveries and mismatched records to responsible teams.",
    icon: Boxes,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Procurement Workflows",
        description:
          "Coordinate purchase requests, approvals and purchase order updates.",
        icon: ClipboardCheck,
      },
      {
        title: "Supplier Coordination",
        description:
          "Organize supplier documents, confirmations and delivery updates.",
        icon: Network,
      },
      {
        title: "Inventory Visibility",
        description:
          "Synchronize stock movements and flag replenishment exceptions.",
        icon: Package,
      },
      {
        title: "Planning & Performance",
        description:
          "Combine operational updates to support planning and reporting.",
        icon: ChartNoAxesCombined,
      },
    ],
    solutions: [
      {
        title: "Purchase-to-Pay Coordination",
        description:
          "Link purchase requests, approvals, order records and invoice checks.",
      },
      {
        title: "Supplier Document Processing",
        description:
          "Collect, validate and route supplier information for review.",
      },
      {
        title: "Inventory Reconciliation",
        description:
          "Compare stock records and send discrepancies to the right team.",
      },
      {
        title: "Supply Chain Exception Desk",
        description:
          "Track late shipments, shortages and unresolved supplier actions.",
      },
    ],
    benefits: [
      "Fewer disconnected supplier handoffs",
      "Earlier visibility of stock and delivery exceptions",
      "More consistent procurement records",
      "Improved coordination across existing systems",
    ],
  },
  {
    slug: "customer-service",
    number: "14",
    title: "Customer Service Solutions",
    shortTitle: "Customer Service",
    subtitle: "Resolve Requests with Less Rework.",
    description:
      "Help service teams respond consistently by automating request intake, case routing, follow-ups and service reporting.",
    overview:
      "CoreRPA connects customer enquiries to the operational teams and systems that resolve them. Routine updates and notifications can be automated while agents retain control over customer conversations and escalations.",
    icon: Mail,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Omnichannel Request Intake",
        description:
          "Capture requests from configured email, web and service channels.",
        icon: Workflow,
      },
      {
        title: "Case Classification & Routing",
        description:
          "Direct requests to the appropriate service team using configured rules.",
        icon: Network,
      },
      {
        title: "Response & Follow-up Tasks",
        description:
          "Prepare routine updates and remind teams about pending responses.",
        icon: ClipboardCheck,
      },
      {
        title: "Service Quality Reporting",
        description:
          "Review request volumes, resolution progress and recurring issues.",
        icon: ChartNoAxesCombined,
      },
    ],
    solutions: [
      {
        title: "Customer Case Management",
        description:
          "Coordinate cases, owners, service status and resolution notes.",
      },
      {
        title: "Enquiry-to-Service Workflow",
        description:
          "Connect customer questions with the right internal service process.",
      },
      {
        title: "Escalation & Notification Automation",
        description:
          "Notify responsible teams when configured service conditions are met.",
      },
      {
        title: "Customer Service Analytics",
        description:
          "Bring service activity and follow-up requirements into clear reports.",
      },
    ],
    benefits: [
      "More consistent request handling",
      "Fewer forgotten follow-ups",
      "Clearer ownership across service teams",
      "Better visibility into customer service workloads",
    ],
  },
  {
    slug: "electricity-grid",
    number: "15",
    title: "Electricity Grid Operations Solutions",
    shortTitle: "Electricity Grid",
    subtitle: "Coordinate Grid Operations with Confidence.",
    description:
      "Support utility administration and field coordination with connected asset, maintenance and service workflows.",
    overview:
      "CoreRPA helps electricity providers and related service organizations coordinate operational records across existing systems. Automation focuses on approved administrative tasks and reporting; it does not directly control grid equipment or protection systems.",
    icon: Zap,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Asset & Maintenance Records",
        description:
          "Keep equipment inventories, inspection schedules and work records aligned.",
        icon: Gauge,
      },
      {
        title: "Outage & Service Coordination",
        description:
          "Route reported service issues and track authorized response updates.",
        icon: Activity,
      },
      {
        title: "Field Work Management",
        description:
          "Coordinate work orders, crew assignments and completion records.",
        icon: Workflow,
      },
      {
        title: "Utility Reporting",
        description:
          "Compile operational updates and flag incomplete submissions.",
        icon: ChartNoAxesCombined,
      },
    ],
    solutions: [
      {
        title: "Utility Work Order Automation",
        description:
          "Coordinate work requests, approvals and field completion updates.",
      },
      {
        title: "Asset Inspection Tracking",
        description:
          "Manage inspection schedules, records and follow-up actions.",
      },
      {
        title: "Customer Service Request Routing",
        description:
          "Direct billing and service enquiries to the appropriate team.",
      },
      {
        title: "Grid Operations Reporting",
        description:
          "Compile authorized operational data for review and reporting.",
      },
    ],
    benefits: [
      "More coordinated field operations",
      "Improved visibility into maintenance work",
      "Less manual compilation of utility reports",
      "Automation separated from direct grid control",
    ],
  },
  {
    slug: "securities",
    number: "16",
    title: "Securities Operations Solutions",
    shortTitle: "Securities",
    subtitle: "Organized Operations. Traceable Reviews.",
    description:
      "Streamline securities administration, investor servicing and operational reporting with controlled, reviewable workflows.",
    overview:
      "CoreRPA supports securities firms and investment operations teams with repeatable document, reconciliation and reporting tasks. Configurable approvals and exception queues help keep staff in control of regulated or high-impact work.",
    icon: ChartNoAxesCombined,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Investor Document Workflows",
        description:
          "Collect, organize and route account and transaction documentation.",
        icon: ClipboardCheck,
      },
      {
        title: "Trade Support Operations",
        description:
          "Coordinate authorized post-trade records and operational checks.",
        icon: Workflow,
      },
      {
        title: "Reconciliation & Exceptions",
        description:
          "Compare operational records and route unmatched items for review.",
        icon: Database,
      },
      {
        title: "Audit & Management Reporting",
        description:
          "Assemble process records and operational reports for authorized users.",
        icon: ShieldCheck,
      },
    ],
    solutions: [
      {
        title: "Investor Onboarding Administration",
        description:
          "Organize application materials and track review completion.",
      },
      {
        title: "Trade Operations Workflow",
        description:
          "Coordinate post-trade records, status updates and exception handling.",
      },
      {
        title: "Portfolio Data Reconciliation",
        description:
          "Compare approved data sources and highlight discrepancies.",
      },
      {
        title: "Securities Operations Reporting",
        description:
          "Prepare repeatable operational reports with traceable source records.",
      },
    ],
    benefits: [
      "More traceable operational workflows",
      "Faster identification of record mismatches",
      "Consistent document and reporting processes",
      "Human approval for sensitive actions",
    ],
  },
  {
    slug: "insurance",
    number: "17",
    title: "Insurance Operations Solutions",
    shortTitle: "Insurance",
    subtitle: "From Policy Requests to Claims Follow-up.",
    description:
      "Connect policy administration, claims documentation and customer service without automating underwriting or claim decisions.",
    overview:
      "CoreRPA helps insurance teams reduce repetitive administrative work across policy servicing, renewals and claims intake. It can organize documents and prepare cases for review while keeping coverage, underwriting and settlement decisions with authorized professionals.",
    icon: ShieldCheck,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Policy Administration",
        description:
          "Coordinate policy updates, renewals and customer documentation.",
        icon: ClipboardCheck,
      },
      {
        title: "Claims Intake & Triage",
        description:
          "Collect submitted documents and route claims to the appropriate reviewers.",
        icon: Workflow,
      },
      {
        title: "Premium & Payment Reconciliation",
        description:
          "Compare payment records and flag unmatched items for follow-up.",
        icon: Wallet,
      },
      {
        title: "Customer Service Operations",
        description:
          "Track enquiries, requests and claim status communications.",
        icon: Users,
      },
    ],
    solutions: [
      {
        title: "Claims Document Processing",
        description:
          "Organize supporting documents and identify incomplete submissions.",
      },
      {
        title: "Policy Renewal Workflow",
        description:
          "Coordinate renewal notices, customer responses and staff follow-up.",
      },
      {
        title: "Insurance Service Desk",
        description:
          "Route policy and claims enquiries with progress tracking.",
      },
      {
        title: "Claims Operations Reporting",
        description:
          "Review processing status, pending documents and unresolved cases.",
      },
    ],
    benefits: [
      "Quicker organization of claims documentation",
      "Fewer missed renewal follow-ups",
      "Clearer visibility into pending cases",
      "Coverage and claims decisions stay with authorized staff",
    ],
  },
  {
    slug: "pan-finance",
    number: "18",
    title: "Enterprise Finance Solutions",
    shortTitle: "Pan-Finance",
    subtitle: "One View Across Finance Operations.",
    description:
      "Connect finance, treasury, accounting and shared-service workflows with practical automation and consolidated operational visibility.",
    overview:
      "For organizations managing finance across teams, entities or business units, CoreRPA can coordinate recurring transactions, records and approvals across existing tools. Flexible workflows support local operating requirements without forcing a single finance process on every team.",
    icon: Wallet,
    accent: "#1683dc",
    capabilities: [
      {
        title: "Accounts Payable & Receivable",
        description:
          "Coordinate invoice intake, payment preparation and receivable follow-up.",
        icon: ClipboardCheck,
      },
      {
        title: "Close & Reconciliation Workflows",
        description:
          "Track close tasks, compare records and route reconciliation exceptions.",
        icon: Workflow,
      },
      {
        title: "Treasury Operations Support",
        description:
          "Organize cash position inputs, approvals and routine reporting tasks.",
        icon: Database,
      },
      {
        title: "Cross-Entity Reporting",
        description:
          "Consolidate approved finance data into repeatable management reports.",
        icon: ChartNoAxesCombined,
      },
    ],
    solutions: [
      {
        title: "Invoice-to-Payment Workflow",
        description:
          "Connect invoice capture, validation, approval and payment preparation.",
      },
      {
        title: "Month-End Close Coordination",
        description:
          "Manage close calendars, task owners and outstanding items.",
      },
      {
        title: "Multi-Entity Reconciliation",
        description:
          "Compare intercompany records and direct differences for review.",
      },
      {
        title: "Finance Operations Dashboard",
        description:
          "Bring recurring workload, approvals and exceptions into one view.",
      },
    ],
    benefits: [
      "More consistent finance processes across teams",
      "Reduced repetitive reconciliation work",
      "Improved visibility into approvals and close tasks",
      "Flexible integration with existing accounting tools",
    ],
  },
];

export function getIndustry(slug: string) {
  return industries.find((industry) => industry.slug === slug);
}