import type { Metadata } from "next";
import Link from "next/link";
import {
  ArrowRight,
  ArrowUpRight,
  BrainCircuit,
  Cloud,
  Code2,
  Container,
  Database,
  GitBranch,
  Headset,
  Layers3,
  Network,
  Server,
  ShieldCheck,
  Workflow,
  Wrench,
} from "lucide-react";

export const metadata: Metadata = {
  title: "Professional Services | ApexiveAI",
  description:
    "Enterprise consulting, managed operations, system integration, and Kubernetes services by ApexiveAI.",
};

const services = [
  {
    number: "01",
    id: "consultation-services",
    icon: BrainCircuit,
    title: "Consultation Services",
    subtitle: "Strategy, Architecture & Digital Transformation",
    description:
      "We help organizations set direction, develop business and product strategies, and plan customer, technology, data, and operational capabilities.",
    categories: [
      {
        title: "Strategic Development",
        items: [
          "Enterprise Strategic Planning",
          "Digital Transformation Planning",
          "Business Development Strategy",
          "Product Development Strategy",
          "Service Development Planning",
          "Enterprise Growth Strategy",
        ],
      },
      {
        title: "Business & Product Consulting",
        items: [
          "Business Model Design",
          "Go-to-Market (GTM) Strategy",
          "Product Pricing Strategy",
          "Tariff Strategy",
          "Product Portfolio Planning",
          "Product Management",
          "Sales Strategy & Coordination",
        ],
      },
      {
        title: "Market & Marketing Consulting",
        items: [
          "Market Research & Analysis",
          "Competitor Analysis",
          "Marketing Strategy",
          "Customer Touchpoint Management",
          "Sales Channel Development",
          "Digital Marketing System Planning",
        ],
      },
      {
        title: "Technology & Platform Consulting",
        items: [
          "Enterprise IT Planning",
          "IT Architecture Assessment",
          "Smart Middle-office Planning",
          "Digital Platform Development Strategy",
          "Business Cloud Services",
          "Data-driven Business Intelligence",
        ],
      },
      {
        title: "Customer Experience Consulting",
        items: [
          "Customer Experience Strategy",
          "Customer History Management",
          "Customer Service Platform Planning",
          "Customer Satisfaction Management",
          "Customer Loyalty Enhancement",
        ],
      },
      {
        title: "Data & Operations Consulting",
        items: [
          "Data Governance Framework",
          "Data Operations Design",
          "Big Data Application Strategy",
          "Data Platform Planning",
          "Data Management Strategy",
        ],
      },
    ],
    outcome: "A clear technology roadmap with measurable business objectives.",
    accent: "blue",
  },
  {
    number: "02",
    id: "operation-services",
    icon: Headset,
    title: "Operation Services",
    subtitle: "Customer Growth, Engagement & Operational Excellence",
    description:
      "We turn customer, product, and operational data into coordinated acquisition, engagement, growth, and public-service operations.",
    categories: [
      {
        title: "Customer Acquisition",
        items: [
          "New Customer Acquisition",
          "Customer Segmentation",
          "Potential Customer Identification",
          "Customer Insight Analysis",
        ],
      },
      {
        title: "Customer Activation & Engagement",
        items: [
          "Customer Activation",
          "Customer Engagement",
          "Customer Retention",
          "Customer Loyalty Improvement",
          "Personalized Customer Campaigns",
        ],
      },
      {
        title: "Business Growth Operations",
        items: [
          "Revenue Growth Operations",
          "Product Sales Enhancement",
          "Cross-selling & Up-selling",
          "Consumer-Product-Scenario Analysis",
          "Business Performance Optimization",
        ],
      },
      {
        title: "Customer Insight & Data Operations",
        items: [
          "360-Degree Customer Insight",
          "Customer Behavior Analysis",
          "Customer Data Analysis",
          "Private Domain Traffic Management",
          "Customer Interaction Tools",
        ],
      },
      {
        title: "Scenario-based Operations",
        items: [
          "Scenario-based Operation Design",
          "Operation Strategy Execution",
          "Campaign Management",
          "Operation Performance Monitoring",
        ],
      },
      {
        title: "Government & City Operations",
        items: [
          "Grid Operation Services",
          "Intelligent Population Insight",
          "Public Management Support",
          "Multi-dimensional Data Analysis",
          "Smart City Management Operations",
        ],
      },
    ],
    outcome: "More engaged customers, measurable growth, and stronger performance.",
    accent: "purple",
  },
  {
    number: "03",
    id: "integration-services",
    icon: Network,
    title: "Integration Services",
    subtitle: "End-to-End Systems, Data & Infrastructure Integration",
    description:
      "We bring software, hardware, networks, and third-party systems together to deliver end-to-end system integration for customers.",
    source: {
      href: "https://www.asiainfo.com/en_us/services.html?utm_source=chatgpt.com",
      label: "AsiaInfo Integration Services",
    },
    categories: [
      {
        title: "Hardware Integration",
        items: [
          "Server Integration",
          "Storage Integration",
          "Network Equipment Integration",
          "Data Center Infrastructure Integration",
          "Hardware Deployment",
        ],
      },
      {
        title: "Software Integration",
        items: [
          "Enterprise Software Integration",
          "ERP Integration",
          "CRM Integration",
          "Database Integration",
          "Business Application Integration",
          "Legacy System Integration",
        ],
      },
      {
        title: "Network Integration",
        items: [
          "LAN/WAN Integration",
          "Enterprise Network Integration",
          "Cloud Network Integration",
          "Network Infrastructure Deployment",
          "Network Connectivity Management",
        ],
      },
      {
        title: "API & Application Integration",
        items: [
          "REST API Integration",
          "SOAP API Integration",
          "Third-party API Integration",
          "Microservices Integration",
          "Application-to-Application Integration",
          "Authentication Integration",
        ],
      },
      {
        title: "Data Integration",
        items: [
          "Database Synchronization",
          "Data Migration",
          "Data Mapping",
          "ETL Integration",
          "Data Exchange",
          "Data Quality Validation",
        ],
      },
      {
        title: "Enterprise Integration Management",
        items: [
          "Integration Architecture Design",
          "Integration Testing",
          "Deployment & Configuration",
          "Technical Documentation",
          "Integration Monitoring",
          "Cost Optimization",
          "Enterprise Technical Standards",
        ],
      },
    ],
    outcome: "Connected systems and consistent data flows across the enterprise.",
    accent: "cyan",
  },
  {
    number: "04",
    id: "kubernetes-services",
    icon: Container,
    title: "Kubernetes-Related Services",
    subtitle: "Container Platforms & Cloud-Native Engineering",
    description:
      "We help organizations plan, deploy, operate, and maintain Kubernetes-based environments for modern enterprise applications and cloud-native workloads.",
    categories: [
      {
        title: "Kubernetes Consulting",
        items: [
          "Kubernetes Adoption Assessment",
          "Kubernetes Architecture Design",
          "Cluster Architecture Planning",
          "Kubernetes Deployment Strategy",
          "Cluster Maintenance Planning",
          "Application Migration Planning",
        ],
      },
      {
        title: "Kubernetes Implementation",
        items: [
          "Customer Requirements Collection",
          "Technical Requirements Analysis",
          "Customized Kubernetes Development",
          "Kubernetes Installation",
          "Cluster Configuration",
          "Kubernetes Project Implementation",
          "Customer Training",
        ],
      },
      {
        title: "Kubernetes Maintenance",
        items: [
          "Cluster Health Monitoring",
          "Troubleshooting",
          "Cluster Scaling",
          "Security Vulnerability Management",
          "Application Service Migration",
          "Infrastructure Maintenance",
          "Cluster Performance Optimization",
        ],
      },
      {
        title: "Business Migration",
        items: [
          "Application Containerization",
          "Legacy Application Migration",
          "Container Workload Migration",
          "Service Deployment Migration",
          "Cloud-native Migration Planning",
        ],
      },
      {
        title: "Resource Management",
        items: [
          "Cluster Resource Management",
          "CPU & Memory Allocation",
          "Container Resource Monitoring",
          "Namespace Management",
          "Workload Resource Management",
        ],
      },
      {
        title: "Application Management",
        items: [
          "Application Deployment",
          "Application Lifecycle Management",
          "Workload Management",
          "Service Discovery",
          "Application Scaling",
          "Application Health Monitoring",
        ],
      },
      {
        title: "Knowledge Transfer & Training",
        items: [
          "Kubernetes Fundamentals Training",
          "Cluster Administration Training",
          "Application Deployment Training",
          "Kubernetes Troubleshooting Training",
          "DevOps & Cloud-native Training",
          "Technical Knowledge Transfer",
        ],
      },
    ],
    outcome: "A manageable container platform designed for scalable workloads.",
    accent: "green",
  },
];

const deliveryStages = [
  {
    icon: BrainCircuit,
    title: "Consult",
    description: "Assess business needs and define the solution.",
  },
  {
    icon: Workflow,
    title: "Implement",
    description: "Build, configure, and deploy enterprise systems.",
  },
  {
    icon: GitBranch,
    title: "Integrate",
    description: "Connect applications, platforms, and data.",
  },
  {
    icon: Wrench,
    title: "Operate",
    description: "Monitor, maintain, and continuously improve.",
  },
];

const deploymentModels = [
  {
    icon: Cloud,
    title: "Cloud",
    description: "Flexible cloud infrastructure and managed services.",
  },
  {
    icon: Server,
    title: "On-Premises",
    description: "Enterprise systems deployed within your own environment.",
  },
  {
    icon: Layers3,
    title: "Hybrid",
    description: "Integrated cloud and on-premises architecture.",
  },
];

export default function ProfessionalServicesPage() {
  return (
    <main className="professional-services">
      <section className="ps-hero">
        <div className="ps-hero-grid" />

        <div className="ps-container ps-hero-content">
          <div className="ps-eyebrow">
            <span className="ps-eyebrow-dot" />
            APEXIVEAI / PROFESSIONAL SERVICES
          </div>

          <h1>
            Enterprise Expertise.
            <br />
            <span>Intelligent Execution.</span>
          </h1>

          <p className="ps-hero-description">
            From technology strategy to implementation, system integration,
            and continuous operations — ApexiveAI helps enterprises build,
            connect, and operate intelligent digital ecosystems.
          </p>

          <div className="ps-hero-actions">
            <a href="#service-portfolio" className="ps-button ps-button-primary">
              Explore Our Services <ArrowRight size={17} />
            </a>

            <a href="#contact" className="ps-button ps-button-outline">
              Discuss Your Project <ArrowUpRight size={17} />
            </a>
          </div>

          <div className="ps-hero-stats">
            <div>
              <strong>04</strong>
              <span>Service Domains</span>
            </div>
            <div>
              <strong>25</strong>
              <span>Service Categories</span>
            </div>
            <div>
              <strong>140</strong>
              <span>Service Offerings</span>
            </div>
          </div>
        </div>

        <div className="ps-hero-visual" aria-hidden="true">
          <div className="ps-orbit ps-orbit-one" />
          <div className="ps-orbit ps-orbit-two" />
          <div className="ps-orbit ps-orbit-three" />

          <div className="ps-core">
            <BrainCircuit size={48} strokeWidth={1.3} />
            <span>APEXIVEAI</span>
            <small>ENTERPRISE INTELLIGENCE</small>
          </div>

          <div className="ps-floating ps-floating-one">
            <Database size={19} />
            <span>DATA</span>
          </div>

          <div className="ps-floating ps-floating-two">
            <Network size={19} />
            <span>INTEGRATION</span>
          </div>

          <div className="ps-floating ps-floating-three">
            <ShieldCheck size={19} />
            <span>SECURITY</span>
          </div>
        </div>
      </section>

      <section className="ps-intro">
        <div className="ps-container ps-intro-grid">
          <div>
            <span className="ps-section-label">OUR PROFESSIONAL SERVICES</span>
            <h2>
              One technology partner.
              <br />
              <span>Four connected service domains.</span>
            </h2>
          </div>

          <p>
            Enterprise transformation requires more than software.
            It requires strategic direction, technical expertise,
            reliable integration, and continuous operational support.
            Our professional services bring these capabilities together
            across 25 categories and 140 specialized offerings.
          </p>
        </div>
      </section>

      <section id="service-portfolio" className="ps-portfolio">
        <div className="ps-container">
          <div className="ps-section-heading">
            <div>
              <span className="ps-section-label">SERVICE PORTFOLIO / 01—04</span>
              <h2>Explore Our Services</h2>
            </div>
            <p>
              Explore our complete service catalog, from strategic consulting
              and customer operations to enterprise integration and Kubernetes.
            </p>
          </div>

          <nav className="ps-service-nav" aria-label="Professional service domains">
            {services.map((service) => (
              <a href={`#${service.id}`} key={service.id}>
                <span>{service.number}</span>
                {service.title}
                <ArrowRight size={15} aria-hidden="true" />
              </a>
            ))}
          </nav>

          <div className="ps-service-grid">
            {services.map((service) => {
              const Icon = service.icon;

              return (
                <article
                  className={`ps-service-card ps-accent-${service.accent}`}
                  id={service.id}
                  key={service.id}
                >
                  <div className="ps-card-top">
                    <div className="ps-service-icon">
                      <Icon size={25} strokeWidth={1.7} />
                    </div>
                    <span className="ps-service-number">{service.number}</span>
                  </div>

                  <h3>{service.title}</h3>
                  <h4>{service.subtitle}</h4>
                  <p className="ps-service-description">
                    {service.description}
                  </p>

                  {"source" in service && service.source && (
                    <a className="ps-service-source" href={service.source.href}>
                      Source: {service.source.label}
                      <ArrowUpRight size={13} aria-hidden="true" />
                    </a>
                  )}

                  <div className="ps-category-grid">
                    {service.categories.map((category) => (
                      <section className="ps-category" key={category.title}>
                        <h4>{category.title}</h4>
                        <ul>
                          {category.items.map((item) => (
                            <li key={item}>
                              <span className="ps-check">✓</span>
                              {item}
                            </li>
                          ))}
                        </ul>
                      </section>
                    ))}
                  </div>

                  <div className="ps-outcome">
                    <ShieldCheck size={18} />
                    <p>{service.outcome}</p>
                  </div>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section className="ps-delivery">
        <div className="ps-container">
          <div className="ps-section-heading ps-delivery-heading">
            <div>
              <span className="ps-section-label">HOW WE WORK</span>
              <h2>End-to-End Service Delivery</h2>
            </div>
            <p>
              A structured delivery lifecycle that connects business strategy
              with real-world implementation and ongoing support.
            </p>
          </div>

          <div className="ps-delivery-grid">
            {deliveryStages.map((stage, index) => {
              const Icon = stage.icon;

              return (
                <div className="ps-delivery-step" key={stage.title}>
                  <div className="ps-step-top">
                    <span>0{index + 1}</span>
                    <Icon size={25} />
                  </div>
                  <h3>{stage.title}</h3>
                  <p>{stage.description}</p>
                  {index !== deliveryStages.length - 1 && (
                    <ArrowRight className="ps-step-arrow" size={20} />
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </section>

      <section className="ps-deployment">
        <div className="ps-container">
          <span className="ps-section-label">DEPLOYMENT FLEXIBILITY</span>
          <h2>
            Built around your
            <br />
            <span>enterprise environment.</span>
          </h2>

          <div className="ps-deployment-grid">
            {deploymentModels.map((model) => {
              const Icon = model.icon;

              return (
                <div className="ps-deployment-card" key={model.title}>
                  <Icon size={27} />
                  <h3>{model.title}</h3>
                  <p>{model.description}</p>
                </div>
              );
            })}
          </div>

          <div className="ps-deployment-note">
            <Code2 size={19} />
            <span>
              Designed for enterprise infrastructure, security requirements,
              and scalable digital operations.
            </span>
          </div>
        </div>
      </section>

      <section id="contact" className="ps-contact">
        <div className="ps-container ps-contact-inner">
          <div>
            <span className="ps-section-label">LET&apos;S BUILD WHAT&apos;S NEXT</span>
            <h2>
              Your enterprise transformation
              <br />
              starts with the right conversation.
            </h2>
            <p>
              Talk to ApexiveAI about your technology roadmap,
              integration requirements, or managed operations needs.
            </p>
          </div>

          <Link href="/contact" className="ps-button ps-button-primary">
            Contact ApexiveAI <ArrowUpRight size={18} />
          </Link>
        </div>
      </section>
    </main>
  );
}