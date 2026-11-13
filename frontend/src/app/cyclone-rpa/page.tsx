import type { Metadata } from "next";
import Link from "next/link";
import {
  ArrowDown,
  ArrowRight,
  ArrowUpRight,
  BadgeCheck,
  Blocks,
  Bot,
  Boxes,
  Check,
  ChevronRight,
  CircleDot,
  Cloud,
  Code2,
  Database,
  FileSpreadsheet,
  Files,
  Fingerprint,
  FolderSync,
  Gauge,
  Globe2,
  KeyRound,
  Mail,
  Monitor,
  Network,
  PackageCheck,
  Play,
  Shield,
  ShieldCheck,
  Workflow,
  Wrench,
} from "lucide-react";
import styles from "@/components/cyclone-rpa/cyclone-rpa.module.css";

export const metadata: Metadata = {
  title: "Cyclone RPA | ApexiveAI",
  description:
    "A standalone enterprise automation platform for designing workflows, managing robot workers and governing business process execution.",
};

const capabilities = [
  {
    number: "01",
    icon: Workflow,
    title: "Visual Workflow Studio",
    subtitle: "Design, test and debug",
    description:
      "Build versioned automation with a visual designer, activity toolbox, workflow debugger and reusable components.",
    tone: "blue",
  },
  {
    number: "02",
    icon: Bot,
    title: "Automation Engine",
    subtitle: "Predictable workflow execution",
    description:
      "Run versioned workflow definitions with controlled retries, execution history, checkpoints and auditable results.",
    tone: "purple",
  },
  {
    number: "03",
    icon: Monitor,
    title: "Windows Robot Runtime",
    subtitle: "Desktop and local execution",
    description:
      "Install a dedicated Windows robot for attended or unattended desktop work and local business-system access.",
    tone: "teal",
  },
  {
    number: "04",
    icon: Network,
    title: "Web Orchestrator",
    subtitle: "Robots, queues and schedules",
    description:
      "Manage workers, dispatch jobs, control schedules, review approvals and monitor execution health in one place.",
    tone: "amber",
  },
];

const businessAutomation = [
  { icon: FileSpreadsheet, title: "Excel & CSV", description: "Read, validate, transform and export tabular business data." },
  { icon: Globe2, title: "Browser automation", description: "Automate approved browser workflows with a dedicated recorder." },
  { icon: FolderSync, title: "Files & folders", description: "Organize files, process documents and manage folder workflows." },
  { icon: Blocks, title: "Web forms", description: "Enter, validate and submit data through repeatable form workflows." },
  { icon: Mail, title: "Email automation", description: "Process messages and attachments with configurable controls." },
];

const deploymentComponents = [
  {
    number: "01",
    icon: Workflow,
    title: "Cyclone Studio",
    label: "DESIGN & DEBUG",
    description: "A separately installable Windows designer for building and testing workflows.",
    href: "/ais-studio",
    action: "Open Studio",
  },
  {
    number: "02",
    icon: Network,
    title: "Cyclone Orchestrator",
    label: "WEB MANAGEMENT",
    description: "A web control plane for robot registration, jobs, schedules and approvals.",
    href: "/automation",
    action: "Open Orchestrator",
  },
  {
    number: "03",
    icon: Monitor,
    title: "Cyclone Runtime",
    label: "WINDOWS ROBOT",
    description: "An independent worker service that executes approved local automation jobs.",
    href: "#architecture",
    action: "View architecture",
  },
  {
    number: "04",
    icon: KeyRound,
    title: "Cyclone License Center",
    label: "ACTIVATION & BILLING",
    description: "Manage licensing requests, subscriptions, activation and renewal workflows.",
    href: "/licenses",
    action: "Open License Center",
  },
];

const architectureLayers = [
  {
    index: "01",
    name: "Studio & Control Plane",
    detail: "Workflow designer · Web orchestrator · License center",
    icon: Workflow,
    tone: "light",
  },
  {
    index: "02",
    name: "Secure API & Job Dispatch",
    detail: "OAuth 2.0 / OIDC · Tenant controls · Queue & heartbeat",
    icon: ShieldCheck,
    tone: "blue",
  },
  {
    index: "03",
    name: "Cyclone Runtime",
    detail: "Windows robot · Browser worker · Local execution",
    icon: Bot,
    tone: "green",
  },
  {
    index: "04",
    name: "Business Systems",
    detail: "Excel · Browser · ERP · CRM · Email · Documents",
    icon: Boxes,
    tone: "light",
  },
];

const roadmap = [
  { number: "01", name: "Product Foundation", details: "Architecture, repository and database", state: "IN PROGRESS" },
  { number: "02", name: "Automation Engine", details: "Versioned workflow execution engine", state: "PLANNED" },
  { number: "03", name: "Windows Runtime", details: "Installable desktop robot", state: "PLANNED" },
  { number: "04", name: "Visual Studio", details: "Drag-and-drop workflow designer", state: "PLANNED" },
  { number: "05", name: "Web Orchestrator", details: "Robot and job management", state: "PLANNED" },
  { number: "06", name: "Enterprise Security", details: "RBAC, audit and encryption", state: "PLANNED" },
  { number: "07", name: "License Center", details: "Online activation and offline licenses", state: "PLANNED" },
  { number: "08", name: "Installer & Updater", details: "Windows installer and managed updates", state: "PLANNED" },
  { number: "09", name: "QA & Pilot", details: "Real business workflow testing", state: "PLANNED" },
  { number: "10", name: "Commercial Release", details: "Customer packages and commercial terms", state: "PLANNED" },
];

const targetStack = [
  { name: "Web Orchestrator", value: "React + TypeScript", icon: Network },
  { name: "Backend API", value: "Django REST Framework", icon: Code2 },
  { name: "Desktop Studio", value: "C# · .NET 10 · WPF", icon: Monitor },
  { name: "Robot Runtime", value: "C# · .NET Worker Service", icon: Bot },
  { name: "Browser Automation", value: "Playwright", icon: Globe2 },
  { name: "Database & Queue", value: "PostgreSQL · Redis", icon: Database },
  { name: "Workflow Contract", value: "Versioned JSON Schema", icon: Workflow },
  { name: "Identity & Hosting", value: "OIDC · Docker · Ownkube", icon: Cloud },
];

const commercialReadiness = [
  { icon: PackageCheck, label: "Windows installer & updater" },
  { icon: BadgeCheck, label: "Code signing & release integrity" },
  { icon: Files, label: "EULA, privacy & data processing terms" },
  { icon: Shield, label: "Security documentation & test report" },
  { icon: Wrench, label: "Installation, user & admin manuals" },
  { icon: Fingerprint, label: "Third-party license compatibility review" },
];

export default function CycloneRpaPage() {
  return (
    <main className={styles.productPage}>
      <section className={styles.hero} id="overview">
        <div className={styles.heroPattern} />
        <div className={styles.contentWidth}>
          <nav className={styles.breadcrumb} aria-label="Breadcrumb">
            <Link href="/">ApexiveAI</Link><ChevronRight size={13} />
            <span>Products</span><ChevronRight size={13} />
            <strong>Cyclone RPA</strong>
          </nav>
          <div className={styles.heroGrid}>
            <div className={styles.heroCopy}>
              <span className={styles.eyebrow}>APEXIVEAI · INTELLIGENT AUTOMATION</span>
              <p className={styles.productNumber}>PRODUCT 24 <span>·</span> CYCLONE SERIES</p>
              <h1>Make work flow.<br /><span>Let robots handle the repeat.</span></h1>
              <p className={styles.heroLead}>
                Cyclone RPA is a standalone automation platform to design,
                deploy and govern business workflows across desktop, browser
                and enterprise systems.
              </p>
              <div className={styles.heroActions}>
                <Link href="/automation" className={styles.buttonPrimary}>
                  Open Orchestrator <ArrowRight size={16} />
                </Link>
                <Link href="/ais-studio" className={styles.buttonSecondary}>
                  Explore Studio <ArrowUpRight size={15} />
                </Link>
              </div>
              <div className={styles.heroFootnote}>
                <ShieldCheck size={15} />
                Independent Studio · Runtime · Orchestrator deployment
              </div>
            </div>
            <div className={styles.heroVisual} aria-label="Cyclone RPA modular platform overview">
              <div className={`${styles.orbit} ${styles.orbitOuter}`} />
              <div className={`${styles.orbit} ${styles.orbitInner}`} />
              <div className={styles.heroCore}>
                <span><Bot size={31} /></span>
                <strong>CYCLONE</strong>
                <small>ROBOTIC PROCESS AUTOMATION</small>
              </div>
              <div className={`${styles.orbitLabel} ${styles.orbitTop}`}><Workflow size={13} /> DESIGN</div>
              <div className={`${styles.orbitLabel} ${styles.orbitRight}`}><Network size={13} /> ORCHESTRATE</div>
              <div className={`${styles.orbitLabel} ${styles.orbitBottom}`}><Bot size={13} /> EXECUTE</div>
              <div className={`${styles.orbitLabel} ${styles.orbitLeft}`}><ShieldCheck size={13} /> GOVERN</div>
              <span className={`${styles.orbitDot} ${styles.dotOne}`} />
              <span className={`${styles.orbitDot} ${styles.dotTwo}`} />
            </div>
          </div>
          <a className={styles.scrollCue} href="#capabilities"><ArrowDown size={14} /> Explore the platform</a>
        </div>
      </section>

      <section className={styles.capabilitiesSection} id="capabilities">
        <div className={styles.contentWidth}>
          <div className={styles.sectionHeading}>
            <div>
              <span className={styles.eyebrow}>A CONNECTED AUTOMATION PLATFORM</span>
              <h2>One platform.<br /><span>Every part of the work.</span></h2>
            </div>
            <p>
              Design, execute and govern business automation with components
              that can be installed and operated independently.
            </p>
          </div>
          <div className={styles.capabilityGrid}>
            {capabilities.map((item) => {
              const Icon = item.icon;
              return (
                <article className={styles.capabilityCard} key={item.number}>
                  <div className={styles.capabilityTop}>
                    <span className={`${styles.capabilityIcon} ${styles[item.tone]}`}><Icon size={20} /></span>
                    <span className={styles.cardNumber}>{item.number}</span>
                  </div>
                  <h3>{item.title}</h3>
                  <strong className={styles.cardSubtitle}>{item.subtitle}</strong>
                  <p>{item.description}</p>
                  <span className={styles.cardRule} />
                </article>
              );
            })}
          </div>

          <div className={styles.businessBlock}>
            <div className={styles.businessHeading}>
              <span className={styles.eyebrow}>AUTOMATE EVERYDAY OPERATIONS</span>
              <h3>Built around the work your teams already do.</h3>
            </div>
            <div className={styles.businessGrid}>
              {businessAutomation.map((item) => {
                const Icon = item.icon;
                return (
                  <article className={styles.businessCard} key={item.title}>
                    <span><Icon size={17} /></span>
                    <div><strong>{item.title}</strong><p>{item.description}</p></div>
                    <Check size={15} className={styles.checkIcon} />
                  </article>
                );
              })}
            </div>
          </div>
        </div>
      </section>

      <section className={styles.workspacesSection} id="workspaces">
        <div className={styles.contentWidth}>
          <div className={styles.sectionHeading}>
            <div>
              <span className={styles.eyebrow}>YOUR PLATFORM, YOUR DEPLOYMENT</span>
              <h2>Four products.<br /><span>One automation lifecycle.</span></h2>
            </div>
            <p>
              Install design tools, robot workers, central management and
              license services according to your security and infrastructure needs.
            </p>
          </div>
          <div className={styles.workspaceGrid}>
            {deploymentComponents.map((item) => {
              const Icon = item.icon;
              return (
                <article className={styles.workspaceCard} key={item.number}>
                  <div className={styles.workspaceTop}>
                    <span className={styles.workspaceIcon}><Icon size={19} /></span>
                    <span>{item.number}</span>
                  </div>
                  <span className={styles.workspaceLabel}>{item.label}</span>
                  <h3>{item.title}</h3>
                  <p>{item.description}</p>
                  <Link href={item.href}>{item.action}<ArrowRight size={14} /></Link>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section className={styles.architectureSection} id="architecture">
        <div className={styles.contentWidth}>
          <div className={styles.architectureGrid}>
            <div className={styles.architectureCopy}>
              <span className={`${styles.eyebrow} ${styles.eyebrowLight}`}>CORE TECHNOLOGY ARCHITECTURE</span>
              <h2>Designed to run<br /><span>where your work lives.</span></h2>
              <p>
                Keep workflow design, control services and robot execution
                separated. Deploy locally, in a private environment or across
                a hybrid infrastructure.
              </p>
              <ul>
                <li><Check size={15} /> Studio, Runtime and Orchestrator can be deployed independently.</li>
                <li><Check size={15} /> Workers communicate through authenticated APIs and job dispatch.</li>
                <li><Check size={15} /> Online activation and offline license options are planned.</li>
              </ul>
              <Link href="/automation" className={styles.architectureLink}>Explore Orchestrator <ArrowUpRight size={15} /></Link>
            </div>
            <div className={styles.architectureStack}>
              {architectureLayers.map((layer, index) => {
                const Icon = layer.icon;
                return (
                  <div key={layer.index}>
                    <article className={`${styles.architectureLayer} ${styles[`layer${layer.index}`]}`}>
                      <span className={styles.layerIcon}><Icon size={18} /></span>
                      <div><span>{layer.index} / PLATFORM LAYER</span><strong>{layer.name}</strong><small>{layer.detail}</small></div>
                      <CircleDot size={13} className={styles.layerStatus} />
                    </article>
                    {index < architectureLayers.length - 1 && <div className={styles.layerConnector}><span /></div>}
                  </div>
                );
              })}
              <div className={styles.architectureCaption}>SECURE BY DESIGN · MODULAR BY DEPLOYMENT</div>
            </div>
          </div>
        </div>
      </section>

      <section className={styles.stackSection}>
        <div className={styles.contentWidth}>
          <div className={styles.sectionHeading}>
            <div>
              <span className={styles.eyebrow}>TARGET TECHNOLOGY STACK</span>
              <h2>Built for a<br /><span>production-ready future.</span></h2>
            </div>
            <p>Planned technology choices for the Cyclone RPA product architecture.</p>
          </div>
          <div className={styles.stackGrid}>
            {targetStack.map((item) => {
              const Icon = item.icon;
              return (
                <article className={styles.stackCard} key={item.name}>
                  <span><Icon size={17} /></span>
                  <div><small>{item.name}</small><strong>{item.value}</strong></div>
                  <ChevronRight size={14} />
                </article>
              );
            })}
          </div>
          <p className={styles.stackNote}>
            Target stack is a product plan; component availability depends on implementation, integration and release validation.
          </p>
        </div>
      </section>

      <section className={styles.roadmapSection} id="roadmap">
        <div className={styles.contentWidth}>
          <div className={styles.sectionHeading}>
            <div>
              <span className={`${styles.eyebrow} ${styles.eyebrowLight}`}>PRODUCT DELIVERY PLAN</span>
              <h2>From foundation<br /><span>to commercial release.</span></h2>
            </div>
            <p>
              A phased roadmap for building, validating and releasing Cyclone
              RPA as an independently deployable product.
            </p>
          </div>
          <div className={styles.roadmapGrid}>
            {roadmap.map((phase) => (
              <article className={styles.phaseCard} key={phase.number}>
                <div className={styles.phaseTop}><span>{phase.number}</span><small>{phase.state}</small></div>
                <h3>{phase.name}</h3>
                <p>{phase.details}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className={styles.licenseSection} id="licensing">
        <div className={styles.contentWidth}>
          <div className={styles.licenseGrid}>
            <div>
              <span className={styles.eyebrow}>ENTERPRISE SECURITY & LICENSING</span>
              <h2>Control the access.<br /><span>Choose your license model.</span></h2>
              <p>
                A hybrid license model is planned to support managed online
                activation and offline deployments where network access is limited.
              </p>
              <Link href="/licenses" className={styles.buttonPrimary}>Visit License Center <ArrowRight size={15} /></Link>
            </div>
            <div className={styles.licenseCards}>
              <article><span><Cloud size={18} /></span><div><strong>Online activation</strong><small>Subscription status and renewal checks through the license service.</small></div><BadgeCheck size={16} /></article>
              <article><span><KeyRound size={18} /></span><div><strong>Offline license</strong><small>Signed license token flow for approved disconnected deployments.</small></div><BadgeCheck size={16} /></article>
              <article><span><Shield size={18} /></span><div><strong>Enterprise controls</strong><small>Tenant roles, audit trail, encryption and execution policies.</small></div><BadgeCheck size={16} /></article>
              <article><span><Gauge size={18} /></span><div><strong>Commercial terms</strong><small>Subscription or perpetual options, subject to commercial release terms.</small></div><BadgeCheck size={16} /></article>
            </div>
          </div>
        </div>
      </section>

      <section className={styles.readinessSection} id="release">
        <div className={styles.contentWidth}>
          <div className={styles.readinessHeader}>
            <div>
              <span className={styles.eyebrow}>RELEASE READINESS</span>
              <h2>Enterprise distribution,<br /><span>with the essentials in place.</span></h2>
            </div>
            <p>Commercial release documentation and operational readiness items are tracked as product deliverables.</p>
          </div>
          <div className={styles.readinessGrid}>
            {commercialReadiness.map((item) => {
              const Icon = item.icon;
              return <div key={item.label}><span><Icon size={17} /></span><strong>{item.label}</strong><small>Release requirement</small></div>;
            })}
          </div>
          <div className={styles.readinessFooter}>
            <ShieldCheck size={16} />
            <span>Installer signing, legal terms, third-party notices and acceptance evidence must be verified before commercial distribution.</span>
          </div>
        </div>
      </section>

      <section className={styles.ctaSection}>
        <div className={styles.contentWidth}>
          <div>
            <span className={styles.eyebrow}>READY TO EXPLORE CYCLONE?</span>
            <h2>Start with the workspace<br /><span>that fits your role.</span></h2>
            <p>Open the Studio to design workflows or the Orchestrator to manage automation operations.</p>
          </div>
          <div className={styles.ctaActions}>
            <Link href="/ais-studio" className={styles.buttonPrimary}><Workflow size={16} /> Open Studio</Link>
            <Link href="/automation" className={styles.buttonLight}><Play size={15} /> Open Orchestrator</Link>
            <Link href="/licenses" className={styles.ctaSubLink}>License Center <ArrowUpRight size={14} /></Link>
          </div>
        </div>
      </section>

      <footer className={styles.footer}>
        <div className={styles.contentWidth}>
          <div className={styles.footerMain}>
            <Link href="/cyclone-rpa" className={styles.brand}>
              <span className={styles.brandMark}><Bot size={20} /></span>
              <span className={styles.brandText}><strong>Cyclone <span>RPA</span></strong><small>APEXIVEAI AUTOMATION</small></span>
            </Link>
            <p>Independent enterprise automation platform.<br />Designed by ApexiveAI.</p>
            <nav aria-label="Cyclone RPA footer navigation">
              <Link href="/ais-studio">Studio</Link>
              <Link href="/automation">Orchestrator</Link>
              <Link href="/licenses">License Center</Link>
              <Link href="/#products">ApexiveAI</Link>
            </nav>
          </div>
          <div className={styles.footerBottom}><span>© 2026 ApexiveAI · Cyclone RPA</span><span>DESIGNED FOR GOVERNED AUTOMATION</span></div>
        </div>
      </footer>
    </main>
  );
}
