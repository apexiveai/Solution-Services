import {
  Activity,
  Bot,
  BrainCircuit,
  ChartNoAxesCombined,
  Code2,
  Cpu,
  Database,
  Gauge,
  Layers3,
  MessageSquareText,
  Network,
  ServerCog,
  ShieldCheck,
  Workflow,
  type LucideIcon,
} from "lucide-react";

export type ProductFamily =
  | "AI & Automation"
  | "Data Intelligence"
  | "Edge & Operations"
  | "Cloud & Network Infrastructure"
  | "Data & Enterprise AI Platform"
  | "Intelligent Automation";

export type Product = {
  slug: string;
  number: string;
  name: string;
  family: ProductFamily;
  tagline: string;
  summary: string;
  overview: string;
  icon: LucideIcon;
  capabilities: { title: string; description: string }[];
  outcomes: string[];
  architecture: { title: string; description: string }[];
};

export const productFamilies: ProductFamily[] = [
  "Cloud & Network Infrastructure",
  "Data & Enterprise AI Platform",
  "AI & Automation",
  "Data Intelligence",
  "Edge & Operations",
  "Intelligent Automation",
];

export const products: Product[] = [
  {
    slug: "vertical-llms",
    number: "01",
    name: "Vertical LLMs",
    family: "AI & Automation",
    tagline: "Domain intelligence, grounded in your enterprise.",
    summary:
      "Purpose-built language model experiences shaped around industry knowledge, operational context and trusted enterprise data.",
    overview:
      "Bring general-purpose AI closer to the work people actually do. Vertical LLMs combine domain terminology, curated knowledge and governed retrieval so teams can explore information and draft useful responses with organizational context.",
    icon: BrainCircuit,
    capabilities: [
      { title: "Domain knowledge", description: "Organize industry terminology, procedures and reference material into reusable knowledge collections." },
      { title: "Grounded responses", description: "Connect answers to approved enterprise sources and make supporting context easier to inspect." },
      { title: "Governed model access", description: "Apply role-aware access and configurable model policies around sensitive information." },
      { title: "Evaluation workflows", description: "Review answer quality with representative questions, feedback and repeatable evaluation sets." },
    ],
    outcomes: ["More relevant answers for specialist teams", "Reusable knowledge across business workflows", "Clearer review and governance of AI-assisted work"],
    architecture: [
      { title: "Experience layer", description: "Role-specific assistants and enterprise applications" },
      { title: "Knowledge & model services", description: "Retrieval, domain context, model routing and evaluation" },
      { title: "Enterprise foundation", description: "Approved data sources, identity controls and audit events" },
    ],
  },
  {
    slug: "tac-maas",
    number: "02",
    name: "TAC MaaS",
    family: "AI & Automation",
    tagline: "A managed path from models to business-ready AI.",
    summary:
      "A model-as-a-service foundation for discovering, evaluating and serving AI capabilities through consistent enterprise interfaces.",
    overview:
      "TAC MaaS helps teams work with a changing AI landscape without scattering model integrations across applications. A shared service layer can expose approved models, route requests and provide the operational controls needed for dependable adoption.",
    icon: Cpu,
    capabilities: [
      { title: "Model access", description: "Present approved foundation and specialist models through a consistent service surface." },
      { title: "Request orchestration", description: "Route requests using policy, capability and deployment requirements." },
      { title: "Lifecycle visibility", description: "Track model versions, evaluation status and operational ownership." },
      { title: "Flexible deployment", description: "Support cloud, private and hybrid model-serving patterns." },
    ],
    outcomes: ["A consistent model integration pattern", "More deliberate model selection and governance", "A foundation teams can extend over time"],
    architecture: [
      { title: "AI applications", description: "Enterprise assistants, agents and domain workflows" },
      { title: "TAC MaaS control plane", description: "Model catalog, policy, routing and service observability" },
      { title: "Model runtime", description: "Approved hosted, private and specialized model endpoints" },
    ],
  },
  {
    slug: "ai-agent-platform",
    number: "03",
    name: "AI Agent Platform",
    family: "AI & Automation",
    tagline: "Design, coordinate and govern enterprise agents.",
    summary:
      "A shared environment for creating task-focused agents that use enterprise tools, knowledge and workflows with clear controls.",
    overview:
      "Move beyond isolated assistants with a platform for composing agents around real operational tasks. Teams can define agent responsibilities, connect approved tools, coordinate human review and observe how work progresses.",
    icon: Bot,
    capabilities: [
      { title: "Agent design", description: "Define goals, instructions, tools and boundaries for purpose-specific agents." },
      { title: "Workflow orchestration", description: "Coordinate multi-step tasks, handoffs and human approval points." },
      { title: "Tool connections", description: "Connect agents to authorized APIs and enterprise services." },
      { title: "Observability & controls", description: "Review activity, outcomes, permissions and operational health." },
    ],
    outcomes: ["Repeatable agent patterns across teams", "Human oversight where decisions require it", "More visible and manageable AI workflows"],
    architecture: [
      { title: "Agent experiences", description: "Embedded assistants and role-based task interfaces" },
      { title: "Agent orchestration", description: "Planning, tools, workflow state and approval controls" },
      { title: "Enterprise services", description: "Identity, knowledge, APIs, policies and audit" },
    ],
  },
  {
    slug: "chatbot",
    number: "04",
    name: "Chatbot",
    family: "AI & Automation",
    tagline: "Helpful conversations, connected to the right service.",
    summary:
      "Conversational experiences for customer and employee support, backed by controlled knowledge and service workflows.",
    overview:
      "Give people a clear conversational entry point to information and services. AEOP Chatbot brings knowledge responses, guided interactions and service handoffs together while keeping operational teams in control of content and escalation paths.",
    icon: MessageSquareText,
    capabilities: [
      { title: "Knowledge conversations", description: "Answer common questions using curated organizational content." },
      { title: "Guided service journeys", description: "Collect the right context and direct users through defined service steps." },
      { title: "Human handoff", description: "Escalate conversations with useful context when a person needs to take over." },
      { title: "Channel-ready design", description: "Shape consistent experiences for web, internal portals and service channels." },
    ],
    outcomes: ["More accessible self-service", "Consistent answers across service touchpoints", "Smoother transitions to human support"],
    architecture: [
      { title: "Conversation channels", description: "Web, employee portal and service entry points" },
      { title: "Conversation services", description: "Intent, knowledge, guided journeys and escalation" },
      { title: "Service foundation", description: "Approved content, customer systems and analytics" },
    ],
  },
  {
    slug: "chatbi",
    number: "05",
    name: "ChatBI",
    family: "Data Intelligence",
    tagline: "Ask better questions of the data you already trust.",
    summary:
      "A conversational analytics experience that helps business users explore governed data and move from questions to insight.",
    overview:
      "ChatBI makes analytics easier to approach without replacing the controls behind trusted reporting. It connects natural-language questions with governed business definitions, relevant datasets and visual explanations that users can review.",
    icon: ChartNoAxesCombined,
    capabilities: [
      { title: "Natural-language exploration", description: "Explore business questions in everyday language and refine follow-up questions." },
      { title: "Governed metrics", description: "Use shared definitions and permissions to keep analysis aligned with business context." },
      { title: "Visual explanations", description: "Present useful charts and summaries alongside the underlying question." },
      { title: "Insight sharing", description: "Help teams share findings and continue analysis from a common starting point." },
    ],
    outcomes: ["More approachable business analytics", "Greater reuse of trusted metrics", "Faster collaboration around operational questions"],
    architecture: [
      { title: "Business experience", description: "Conversational analysis, visual answers and shared insights" },
      { title: "Semantic analytics", description: "Business vocabulary, governed metrics and query services" },
      { title: "Connected data", description: "Approved warehouses, lakehouses and operational sources" },
    ],
  },
  {
    slug: "aiops-agents",
    number: "06",
    name: "AIOps Agents",
    family: "AI & Automation",
    tagline: "Turn operational signals into coordinated action.",
    summary:
      "AI-assisted operations for detecting patterns, understanding service impact and coordinating incident response.",
    overview:
      "AIOps Agents bring operational events and service context together to help teams investigate issues with less context switching. Agents can surface related signals and recommend next steps while operators retain control over remediation.",
    icon: Activity,
    capabilities: [
      { title: "Signal correlation", description: "Bring together alerts, changes and service context for a clearer operational picture." },
      { title: "Incident assistance", description: "Summarize relevant events and guide investigation with operational knowledge." },
      { title: "Workflow coordination", description: "Support triage, escalation and response steps across operations teams." },
      { title: "Human-controlled actions", description: "Keep approvals and operator decisions explicit for consequential changes." },
    ],
    outcomes: ["Clearer incident context", "More coordinated response workflows", "Safer adoption of AI in live operations"],
    architecture: [
      { title: "Operations workspace", description: "Service views, incident timelines and response collaboration" },
      { title: "AIOps intelligence", description: "Correlation, context enrichment and agent assistance" },
      { title: "Operational telemetry", description: "Events, metrics, logs, topology and change records" },
    ],
  },
  {
    slug: "autoagent",
    number: "07",
    name: "AutoAgent",
    family: "AI & Automation",
    tagline: "Automate the work between your enterprise systems.",
    summary:
      "A governed automation workspace for mapping, operating and improving repeatable business processes.",
    overview:
      "AutoAgent connects repeatable work across applications, teams and business rules. It helps organizations structure automations, coordinate attended and unattended steps, and keep exception handling visible instead of hiding it in brittle scripts.",
    icon: Workflow,
    capabilities: [
      { title: "Process orchestration", description: "Model tasks, branching logic, schedules and handoffs as manageable workflows." },
      { title: "Application automation", description: "Connect approved application actions and process steps." },
      { title: "Exception handling", description: "Route failures and edge cases to the right operators with process context." },
      { title: "Automation governance", description: "Track ownership, execution status and change history for automations." },
    ],
    outcomes: ["More consistent execution of repeatable work", "Better visibility into exceptions and process health", "A maintainable automation portfolio"],
    architecture: [
      { title: "Business workflows", description: "Process entry points, tasks and human approvals" },
      { title: "Automation runtime", description: "Orchestration, connectors, schedules and exception handling" },
      { title: "Enterprise applications", description: "Authorized APIs, systems of record and desktop workflows" },
    ],
  },
  {
    slug: "turing-dev-suite",
    number: "08",
    name: "TuringDevSuite",
    family: "AI & Automation",
    tagline: "A more connected workspace for modern software delivery.",
    summary:
      "Developer tools and AI-assisted workflows that support teams from planning and coding through review and release.",
    overview:
      "TuringDevSuite brings developer productivity capabilities into a cohesive delivery experience. Teams can use AI assistance in context, connect work to engineering processes and apply their own review, security and quality standards.",
    icon: Code2,
    capabilities: [
      { title: "AI-assisted development", description: "Support coding, explanation and documentation tasks inside engineering workflows." },
      { title: "Delivery collaboration", description: "Connect engineering work with planning, review and release activities." },
      { title: "Quality practices", description: "Keep checks and team standards visible throughout the delivery lifecycle." },
      { title: "Enterprise controls", description: "Align developer tooling with organizational access and governance requirements." },
    ],
    outcomes: ["Less fragmented developer tooling", "AI assistance aligned with team workflows", "More consistent engineering practices"],
    architecture: [
      { title: "Developer workspace", description: "Coding, review, planning and delivery experiences" },
      { title: "Engineering intelligence", description: "AI assistance, workflow context and quality signals" },
      { title: "Delivery ecosystem", description: "Repositories, CI/CD, issue tracking and approved models" },
    ],
  },
  {
    slug: "edge-intelligence",
    number: "09",
    name: "AI² Edge Intelligence",
    family: "Edge & Operations",
    tagline: "Bring intelligence closer to where operations happen.",
    summary:
      "An edge AI foundation for connecting devices, processing local signals and coordinating with enterprise platforms.",
    overview:
      "AI² Edge Intelligence supports operational environments where latency, connectivity and local context matter. It helps teams coordinate edge workloads and device data with central governance and enterprise analytics.",
    icon: Network,
    capabilities: [
      { title: "Edge workload management", description: "Organize edge applications and deployment groups across distributed sites." },
      { title: "Local intelligence", description: "Support inference and event processing close to operational data sources." },
      { title: "Device connectivity", description: "Connect authorized devices, gateways and industrial data feeds." },
      { title: "Central visibility", description: "Monitor distributed environments with enterprise-level policies and status." },
    ],
    outcomes: ["Responsive intelligence in distributed settings", "A clearer view of edge assets and workloads", "A governed bridge between edge and cloud"],
    architecture: [
      { title: "Operational applications", description: "Local insights, alerts and edge-enabled workflows" },
      { title: "Edge intelligence layer", description: "Workload coordination, device services and local AI" },
      { title: "Connected enterprise", description: "Central policy, analytics, identity and lifecycle controls" },
    ],
  },
  {
    slug: "ontology-platform",
    number: "10",
    name: "Ontology Platform",
    family: "Data Intelligence",
    tagline: "Give enterprise data a shared operational meaning.",
    summary:
      "A semantic foundation for connecting business concepts, data assets and operational relationships across systems.",
    overview:
      "The Ontology Platform helps organizations describe how important business entities relate and how teams use them. A shared semantic layer can make data easier to discover, interpret and reuse across analytics and operational applications.",
    icon: Layers3,
    capabilities: [
      { title: "Business concept modeling", description: "Represent core entities, relationships and business terminology." },
      { title: "Source mapping", description: "Connect semantic concepts to approved data assets and operational systems." },
      { title: "Knowledge discovery", description: "Explore relationships and understand where information is used." },
      { title: "Governed reuse", description: "Make definitions and ownership clearer across data products and teams." },
    ],
    outcomes: ["More consistent business definitions", "Discoverable relationships across data", "A reusable semantic foundation for AI and analytics"],
    architecture: [
      { title: "Business applications", description: "AI, analytics and operational tools using shared meaning" },
      { title: "Ontology services", description: "Concepts, relationships, mappings and semantic APIs" },
      { title: "Enterprise data", description: "Governed systems, data products and knowledge sources" },
    ],
  },
  {
    slug: "dataatlas",
    number: "11",
    name: "DataAtlas",
    family: "Data Intelligence",
    tagline: "Know what data you have, where it lives and how it is used.",
    summary:
      "A data discovery and governance workspace for understanding enterprise assets, lineage, ownership and quality.",
    overview:
      "DataAtlas creates a navigable view of an organization's data landscape. By improving discovery, stewardship and lineage visibility, teams can build trust in data assets and make informed decisions about how they are used.",
    icon: Database,
    capabilities: [
      { title: "Data catalog", description: "Discover datasets and key assets across connected sources." },
      { title: "Lineage context", description: "Understand relationships between source data, transformations and downstream use." },
      { title: "Stewardship", description: "Make ownership, descriptions and governance responsibilities visible." },
      { title: "Quality signals", description: "Surface quality context to help users assess whether data fits a purpose." },
    ],
    outcomes: ["Faster discovery of relevant data", "More transparent lineage and ownership", "Better-informed data reuse"],
    architecture: [
      { title: "Data consumers", description: "Business teams, analysts and AI applications" },
      { title: "DataAtlas catalog", description: "Discovery, lineage, stewardship and quality context" },
      { title: "Connected sources", description: "Warehouses, lakehouses, databases and business systems" },
    ],
  },
  {
    slug: "dataflux",
    number: "12",
    name: "DataFlux",
    family: "Data Intelligence",
    tagline: "Move and shape data with confidence across the enterprise.",
    summary:
      "A data integration and pipeline workspace for connecting sources, transforming information and monitoring data movement.",
    overview:
      "DataFlux helps engineering and analytics teams manage the flow of information between systems. Reusable ingestion patterns, transformation steps and operational visibility support dependable data products across a hybrid environment.",
    icon: Workflow,
    capabilities: [
      { title: "Source integration", description: "Connect databases, applications, files and event-based sources." },
      { title: "Pipeline design", description: "Compose data movement and transformation steps into reusable flows." },
      { title: "Operational monitoring", description: "Review run status, failures and data delivery health." },
      { title: "Hybrid connectivity", description: "Support integration patterns across cloud and on-premises environments." },
    ],
    outcomes: ["More manageable data movement", "Improved visibility into pipeline health", "Reusable integration patterns for data teams"],
    architecture: [
      { title: "Data products", description: "Curated information for analytics, applications and AI" },
      { title: "DataFlux pipelines", description: "Ingestion, transformation, scheduling and monitoring" },
      { title: "Enterprise sources", description: "Operational applications, databases, files and events" },
    ],
  },
  {
    slug: "intelligent-operation",
    number: "13",
    name: "IO — Intelligent Operation",
    family: "Edge & Operations",
    tagline: "A connected command view for complex operations.",
    summary:
      "An operational intelligence workspace combining service context, performance signals and coordinated decision support.",
    overview:
      "IO connects operational information that is often spread across teams and systems. It gives operators a shared view of important signals, workflows and service context so they can coordinate decisions and follow outcomes.",
    icon: Gauge,
    capabilities: [
      { title: "Operational command view", description: "Bring key services, processes and current conditions into one workspace." },
      { title: "Performance intelligence", description: "Track operational indicators and explore patterns over time." },
      { title: "Decision workflows", description: "Coordinate actions, ownership and follow-up across teams." },
      { title: "Enterprise integration", description: "Connect relevant operational systems through governed interfaces." },
    ],
    outcomes: ["A shared operational picture", "More coordinated decisions across teams", "Clearer accountability from signal to action"],
    architecture: [
      { title: "Operations workspace", description: "Command views, KPIs, collaboration and action tracking" },
      { title: "Intelligence services", description: "Context, analytics, workflow and decision support" },
      { title: "Operational systems", description: "Enterprise applications, service platforms and telemetry" },
    ],
  },
  {
    slug: "apexive-netmatrix",
    number: "14",
    name: "Apexive NetMatrix",
    family: "Cloud & Network Infrastructure",
    tagline: "Autonomous Network Engine",
    summary:
      "AI-assisted traffic routing and network load balancing for telecom and internet operators.",
    overview:
      "NetMatrix is an AEOP network-engine concept for operators who need a unified view of traffic, capacity and service paths. Its design brings routing intelligence, load distribution and operator oversight into one operational workflow.",
    icon: Network,
    capabilities: [
      { title: "Traffic intelligence", description: "Analyze network conditions and traffic patterns to inform routing decisions." },
      { title: "Load balancing", description: "Distribute network demand across available paths and resources using configurable policies." },
      { title: "Operator controls", description: "Keep policy changes, recommendations and operational approvals visible to network teams." },
      { title: "Service-aware routing", description: "Bring service priorities and network health context into traffic-management workflows." },
    ],
    outcomes: ["A clearer view of network demand", "More consistent traffic-management workflows", "Operator-governed routing recommendations"],
    architecture: [
      { title: "Network operations workspace", description: "Traffic views, routing policies and operator approvals" },
      { title: "NetMatrix intelligence", description: "Network signals, decision support and load-balancing workflows" },
      { title: "Connected infrastructure", description: "Operator-managed network devices, links and telemetry" },
    ],
  },
  {
    slug: "apexive-pulse",
    number: "15",
    name: "Apexive Pulse",
    family: "Cloud & Network Infrastructure",
    tagline: "Network Performance & Customer Experience",
    summary:
      "A real-time operations view for network health, quality of experience and customer experience management.",
    overview:
      "Pulse is designed to help service teams connect network performance with the experience customers receive. The workspace brings service health, QoE indicators and customer-experience context together so teams can investigate issues with a shared operational picture.",
    icon: Activity,
    capabilities: [
      { title: "Network health", description: "Monitor service and infrastructure indicators in a consolidated operational view." },
      { title: "Quality of experience", description: "Explore QoE signals alongside service and network performance context." },
      { title: "Customer experience", description: "Connect customer-impact indicators with network and service events." },
      { title: "Performance dashboards", description: "Configure role-based views for operations, service assurance and experience teams." },
    ],
    outcomes: ["Shared visibility across network and customer experience", "Earlier awareness of service degradation", "More context for service-assurance decisions"],
    architecture: [
      { title: "Experience dashboards", description: "Network health, QoE and customer-impact views" },
      { title: "Pulse intelligence", description: "Signal correlation, service context and performance analytics" },
      { title: "Operational data", description: "Network telemetry, service events and experience indicators" },
    ],
  },
  {
    slug: "apexive-faultguard",
    number: "16",
    name: "Apexive FaultGuard",
    family: "Cloud & Network Infrastructure",
    tagline: "Predictive Fault & Incident Management",
    summary:
      "A predictive operations concept for identifying potential network failures and coordinating timely alerts.",
    overview:
      "FaultGuard is designed to bring outage signals, failure patterns and incident response into one workflow. Predictive analytics can help operators prioritize emerging risks, while alerting and response actions remain traceable and governed by the operations team.",
    icon: ShieldCheck,
    capabilities: [
      { title: "Failure-pattern analysis", description: "Review historical and current signals for patterns associated with network faults." },
      { title: "Predictive risk indicators", description: "Surface potential service risks for operator assessment before they become incidents." },
      { title: "Automated alert workflows", description: "Route configurable alerts to the teams responsible for investigation." },
      { title: "Incident coordination", description: "Track fault context, ownership and response status in a shared workflow." },
    ],
    outcomes: ["Earlier visibility into potential network faults", "More consistent incident alerting", "Traceable response coordination"],
    architecture: [
      { title: "Incident workspace", description: "Risk views, alerts, ownership and response tracking" },
      { title: "FaultGuard analytics", description: "Pattern analysis, risk scoring and configurable alert rules" },
      { title: "Network signals", description: "Events, alarms, performance indicators and service topology" },
    ],
  },
  {
    slug: "apexive-omni-orchestrator",
    number: "17",
    name: "Apexive OmniOrchestrator",
    family: "Cloud & Network Infrastructure",
    tagline: "Unified Network & Cloud Orchestration",
    summary:
      "A unified orchestration framework concept for hybrid cloud, SDN and multi-vendor telecom infrastructure.",
    overview:
      "OmniOrchestrator is designed to give infrastructure teams a consistent place to coordinate services across hybrid cloud and multi-vendor network environments. It focuses on policy-aware workflows, resource visibility and controlled orchestration across connected domains.",
    icon: Workflow,
    capabilities: [
      { title: "Hybrid cloud coordination", description: "Model service workflows across connected cloud and on-premises environments." },
      { title: "SDN orchestration", description: "Coordinate network service changes through defined, reviewable workflows." },
      { title: "Multi-vendor resource view", description: "Bring infrastructure resources from different vendors into a consistent operations view." },
      { title: "Policy-aware automation", description: "Apply approvals, change controls and execution visibility to orchestration tasks." },
    ],
    outcomes: ["One operational view across infrastructure domains", "More repeatable service orchestration", "Clearer controls for cross-vendor changes"],
    architecture: [
      { title: "Service orchestration", description: "Service requests, workflows and change approvals" },
      { title: "OmniOrchestrator control layer", description: "Policy, resource coordination and vendor adapters" },
      { title: "Hybrid infrastructure", description: "Cloud platforms, SDN domains and telecom network resources" },
    ],
  },
  {
    slug: "apexive-ai-core",
    number: "18",
    name: "Apexive AI Core",
    family: "Data & Enterprise AI Platform",
    tagline: "Enterprise AI Platform",
    summary:
      "A central platform concept for deploying and managing enterprise AI models, language models and automation workflows.",
    overview:
      "AI Core is designed as a shared enterprise foundation for teams that need to manage AI capabilities across applications. A central workspace can coordinate model access, deployment workflows and RPA automations with the governance and operational visibility needed by enterprise teams.",
    icon: BrainCircuit,
    capabilities: [
      { title: "AI model lifecycle", description: "Organize model registration, evaluation, deployment and operational ownership." },
      { title: "Enterprise LLM services", description: "Connect approved language-model capabilities to enterprise applications and knowledge." },
      { title: "RPA workflow management", description: "Design, deploy and monitor automation workflows through a shared control surface." },
      { title: "Governance and observability", description: "Track access, deployment state and operational activity across AI services." },
    ],
    outcomes: ["A shared control plane for AI adoption", "More consistent model and workflow operations", "Clearer governance across AI deployments"],
    architecture: [
      { title: "Enterprise AI applications", description: "Agents, assistants, analytics and automation experiences" },
      { title: "AI Core platform", description: "Model services, workflow management and deployment controls" },
      { title: "Enterprise foundation", description: "Identity, data sources, infrastructure and audit" },
    ],
  },
  {
    slug: "apexive-chatnexus",
    number: "19",
    name: "Apexive ChatNexus",
    family: "Data & Enterprise AI Platform",
    tagline: "Localized Enterprise ChatCRM",
    summary:
      "An omnichannel CRM and conversational platform designed for Myanmar-language customer interactions and enterprise workflows.",
    overview:
      "ChatNexus is designed around local customer-service needs, with a focus on Myanmar-language conversations, Unicode and Zawgyi text handling, and configurable support for regional language requirements. Its CRM and chatbot workflows connect customer context, service conversations and human handoff in one experience.",
    icon: MessageSquareText,
    capabilities: [
      { title: "Myanmar-language conversations", description: "Design natural conversational flows for Myanmar-language customer service." },
      { title: "Unicode and Zawgyi handling", description: "Support text normalization and conversion workflows for mixed legacy and modern Myanmar text." },
      { title: "Omnichannel CRM", description: "Bring customer conversations and service history together across configured channels." },
      { title: "Regional language readiness", description: "Provide an extensible language layer for additional ethnic and regional language support." },
    ],
    outcomes: ["More consistent customer conversations across channels", "A unified view of service context", "A localization-ready conversational foundation"],
    architecture: [
      { title: "Customer service channels", description: "Web, messaging, contact center and agent experiences" },
      { title: "ChatNexus conversation layer", description: "Language processing, CRM context, chatbot flows and human handoff" },
      { title: "Enterprise services", description: "Customer records, service workflows and approved knowledge sources" },
    ],
  },
  {
    slug: "apexive-dataengine",
    number: "20",
    name: "Apexive DataEngine",
    family: "Data & Enterprise AI Platform",
    tagline: "Cloud Server & Middleware",
    summary:
      "A scalable infrastructure concept for high-concurrency services and enterprise microservice workloads.",
    overview:
      "DataEngine is designed as an infrastructure foundation for enterprise applications that need reliable throughput as demand grows. Its server and middleware layers emphasize scalable service patterns, workload visibility and flexible deployment across enterprise environments.",
    icon: ServerCog,
    capabilities: [
      { title: "High-concurrency service patterns", description: "Support application architectures designed for concurrent enterprise workloads." },
      { title: "Scalable microservices", description: "Provide reusable runtime patterns for independently managed services." },
      { title: "Middleware services", description: "Coordinate application connectivity and shared platform components." },
      { title: "Deployment visibility", description: "Expose service health and workload status across configured environments." },
    ],
    outcomes: ["A more consistent application runtime foundation", "Scalable patterns for enterprise services", "Improved visibility across middleware workloads"],
    architecture: [
      { title: "Enterprise applications", description: "Business services and API-driven workloads" },
      { title: "DataEngine runtime", description: "Server services, middleware and microservice coordination" },
      { title: "Deployment foundation", description: "Cloud, private infrastructure and operational telemetry" },
    ],
  },
  {
    slug: "apexive-twin",
    number: "21",
    name: "Apexive Twin",
    family: "Data & Enterprise AI Platform",
    tagline: "Digital Twin Engine",
    summary:
      "A digital-twin platform concept for modeling enterprise processes, logistics flows and physical assets.",
    overview:
      "Apexive Twin is designed to create a digital representation of operational processes and physical assets. Connected data and simulation workflows help teams explore scenarios, understand dependencies and evaluate potential operational changes before acting in the real environment.",
    icon: Layers3,
    capabilities: [
      { title: "Asset modeling", description: "Represent physical assets and their operational relationships in a digital model." },
      { title: "Process simulation", description: "Explore process flows and operational scenarios using connected business context." },
      { title: "Logistics visibility", description: "Model movement, dependencies and status across logistics operations." },
      { title: "Scenario analysis", description: "Compare possible changes and review their modeled operational implications." },
    ],
    outcomes: ["A connected view of assets and processes", "More informed scenario planning", "Better understanding of operational dependencies"],
    architecture: [
      { title: "Twin experiences", description: "Operational dashboards, scenario exploration and collaboration" },
      { title: "Apexive Twin engine", description: "Models, simulation workflows and relationship context" },
      { title: "Connected operations", description: "Asset telemetry, logistics systems and enterprise process data" },
    ],
  },
  {
    slug: "apexive-secureshield",
    number: "22",
    name: "Apexive SecureShield",
    family: "Data & Enterprise AI Platform",
    tagline: "Telecom & Enterprise SBC Security",
    summary:
      "A security platform concept combining session-border control workflows and threat-detection interfaces.",
    overview:
      "SecureShield is designed for telecom and enterprise environments that need stronger visibility at communication and service boundaries. The concept combines SBC-oriented control with threat-detection signals and APIs that can connect security observations to existing operational response processes.",
    icon: ShieldCheck,
    capabilities: [
      { title: "Session border control", description: "Manage communication-boundary policies and service visibility through an SBC-oriented workflow." },
      { title: "Threat signal analysis", description: "Surface security indicators for review by enterprise and telecom operations teams." },
      { title: "Security APIs", description: "Provide integration interfaces for connecting detection context to approved security systems." },
      { title: "Response coordination", description: "Link security events to ownership, investigation and incident workflows." },
    ],
    outcomes: ["Clearer visibility at service boundaries", "More connected threat investigation workflows", "A foundation for integrating security signals"],
    architecture: [
      { title: "Security operations", description: "Threat views, investigations and response coordination" },
      { title: "SecureShield services", description: "SBC policy workflows, signal analysis and security APIs" },
      { title: "Protected environments", description: "Telecom services, enterprise networks and connected systems" },
    ],
  },
  {
    slug: "apexive-apexdb",
    number: "23",
    name: "Apexive ApexDB",
    family: "Data & Enterprise AI Platform",
    tagline: "Distributed Relational & Vector Database",
    summary:
      "A database-engine concept for highly available relational, vector and analytics workloads.",
    overview:
      "ApexDB is designed as a locally developed database direction for enterprise data, AI and analytics workloads. Its proposed architecture brings distributed relational storage and vector-search patterns together, with an emphasis on high availability, performance evaluation and deployment choice.",
    icon: Database,
    capabilities: [
      { title: "Distributed relational data", description: "Organize transactional data across a distributed database architecture." },
      { title: "Vector search foundation", description: "Support vector indexing and retrieval patterns for AI-enabled applications." },
      { title: "High-availability design", description: "Plan for resilient service continuity and operational recovery." },
      { title: "Analytics workload support", description: "Evaluate data-access patterns for large-scale reporting and AI workloads." },
    ],
    outcomes: ["One data foundation for relational and AI patterns", "More deployment options for enterprise data", "A clear direction for local database innovation"],
    architecture: [
      { title: "Data applications", description: "Enterprise systems, AI retrieval and analytics" },
      { title: "ApexDB engine", description: "Distributed SQL, vector services and availability controls" },
      { title: "Data infrastructure", description: "Managed compute, storage, backup and monitoring" },
    ],
  },
  {
    slug: "apexive-cyclone-rpa",
    number: "24",
    name: "Apexive CoreRPA",
    family: "Intelligent Automation",
    tagline: "Governed automation for connected enterprise work.",
    summary:
      "Design, orchestrate and monitor human-guided automations across approved enterprise workflows.",
    overview:
      "Apexive CoreRPA brings workflow design, bot operations, task queues, approvals, license governance and execution monitoring into one enterprise automation platform.",
    icon: Bot,
    capabilities: [
      { title: "Visual workflow design", description: "Compose versioned workflows from reusable, allow-listed steps, conditions and controlled loops." },
      { title: "Bot orchestration", description: "Register workers, assign workloads and monitor bot health with explicit lifecycle controls." },
      { title: "Human approvals", description: "Route sensitive workflow steps to named reviewers and retain the approval history." },
      { title: "Governed operations", description: "Apply tenant boundaries, role permissions, execution limits and searchable audit trails." },
    ],
    outcomes: [
      "Automate repeatable work with traceable workflow versions",
      "Keep exceptions and approval decisions visible to operators",
      "Scale automation within tenant-specific execution policies",
    ],
    architecture: [
      { title: "Design & governance", description: "Versioned workflows, roles, approvals and tenant policies" },
      { title: "Orchestration", description: "Bots, queues, schedules, triggers and monitored executions" },
      { title: "Approved integrations", description: "Registered connectors for enterprise applications and data" },
    ],
  },
];

export function getProduct(slug: string) {
  return products.find((product) => product.slug === slug);
}

export const productNavigationGroups = [
  {
    title: "AI & Automation",
    brand: "Apexive Intelligence",
    description:
      "AI and automation tools adapted to the workflows and technology environments of Myanmar organizations.",
    family: "AI & Automation",
  },
  {
    title: "Data Intelligence",
    brand: "Apexive DataCraft",
    description:
      "Data discovery, integration and analytics for local business teams.",
    family: "Data Intelligence",
  },
  {
    title: "Cloud & Network Infrastructure",
    brand: "Apexive InfraTech",
    description:
      "Network operations and service platforms for Myanmar telecom, internet and cloud providers.",
    family: "Cloud & Network Infrastructure",
  },
  {
    title: "Data & Enterprise AI Platform",
    brand: "Apexive DataCraft",
    description:
      "Enterprise AI, customer engagement and data foundations for Myanmar organizations.",
    family: "Data & Enterprise AI Platform",
  },
  {
    title: "Edge & Operations",
    brand: "Apexive Operations",
    description:
      "Operational intelligence and edge capabilities for connected teams and sites.",
    family: "Edge & Operations",
  },
  {
    title: "Intelligent Automation",
    brand: "Apexive CoreRPA",
    description:
      "Locally developed workflow automation with governed bot orchestration and execution visibility.",
    family: "Intelligent Automation",
  },
] satisfies { title: string; brand: string; description: string; family: ProductFamily }[];
