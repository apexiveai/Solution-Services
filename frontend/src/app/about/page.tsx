
import Link from "next/link";
import {
  ArrowRight,
  ArrowUpRight,
  BrainCircuit,
  Cloud,
  Database,
  Network,
  ShieldCheck,
  Workflow,
  Globe2,
  Layers3,
  Target,
  Eye,
  Lightbulb,
} from "lucide-react";
import styles from "./about.module.css";

const infraProducts = [
  {
    name: "Apexive NetMatrix",
    category: "AUTONOMOUS NETWORK ENGINE",
    description:
      "AI-driven traffic routing and network load balancing for intelligent network operations.",
    icon: Network,
  },
  {
    name: "Apexive Pulse",
    category: "NETWORK PERFORMANCE & CEM",
    description:
      "Real-time network health, QoE and Customer Experience Management dashboard.",
    icon: ActivityIcon,
  },
  {
    name: "Apexive FaultGuard",
    category: "FAULT & INCIDENT MANAGEMENT",
    description:
      "Predictive analytics and automated alerts for network outages and infrastructure failures.",
    icon: ShieldCheck,
  },
  {
    name: "Apexive OmniOrchestrator",
    category: "NETWORK RESOURCE & ORCHESTRATION",
    description:
      "A unified orchestration framework for hybrid cloud, SDN and multi-vendor telecom infrastructure.",
    icon: Workflow,
  },
];

const dataProducts = [
  {
    name: "Apexive AI Core",
    category: "ENTERPRISE PAAS",
    description:
      "A central platform to deploy and manage enterprise AI models, LLMs and RPA workflows.",
    icon: BrainCircuit,
  },
  {
    name: "Apexive ChatNexus",
    category: "LOCALIZED ENTERPRISE CHATCRM",
    description:
      "An omnichannel CRM and chatbot engine designed for Myanmar language processing and localized communication.",
    icon: Globe2,
  },
  {
    name: "Apexive DataEngine",
    category: "CLOUD SERVER & MIDDLEWARE",
    description:
      "Scalable server infrastructure and middleware for high-concurrency enterprise applications.",
    icon: Cloud,
  },
  {
    name: "Apexive Twin",
    category: "DIGITAL TWIN ENGINE",
    description:
      "AI-powered simulation of enterprise processes, logistics and physical assets.",
    icon: Layers3,
  },
  {
    name: "Apexive SecureShield",
    category: "ENTERPRISE SECURITY & SBC",
    description:
      "Session Border Controller capabilities and enterprise security threat detection APIs.",
    icon: ShieldCheck,
  },
  {
    name: "Apexive ApexDB",
    category: "DISTRIBUTED DATABASE ENGINE",
    description:
      "A Made in Burma database initiative for high-availability relational, vector and analytics workloads.",
    icon: Database,
  },
];

function ActivityIcon({ size = 20 }: { size?: number }) {
  return <Target size={size} />;
}

function ProductCard({
  product,
}: {
  product: (typeof infraProducts)[number] | (typeof dataProducts)[number];
}) {
  const Icon = product.icon;

  return (
    <article className={styles.productCard}>
      <div className={styles.productIcon}>
        <Icon size={21} strokeWidth={1.7} />
      </div>
      <span className={styles.productCategory}>{product.category}</span>
      <h3>{product.name}</h3>
      <p>{product.description}</p>
      <span className={styles.productLine} />
    </article>
  );
}

export const metadata = {
  title: "About ApexiveAI | Enterprise Technology Company",
  description:
    "Discover ApexiveAI, our technology divisions, enterprise platforms and vision for intelligent digital transformation.",
};

export default function AboutPage() {
  return (
    <div className={styles.aboutPage}>
      <section className={styles.hero}>
        <div className={styles.heroGrid} />
        <div className={styles.heroContent}>
          <span className={styles.eyebrow}>ABOUT APEXIVEAI</span>
          <h1>
            Engineering intelligence.
            <br />
            <span>Enabling transformation.</span>
          </h1>
          <p>
            Building intelligent enterprise technologies across cloud
            infrastructure, telecommunications, data platforms and artificial
            intelligence.
          </p>
          <div className={styles.heroActions}>
            <Link href="/contact" className={styles.primaryButton}>
              Connect with us <ArrowRight size={17} />
            </Link>
            <span className={styles.heroNote}>
              INTELLIGENCE IN MOTION.
            </span>
          </div>
        </div>
        <div className={styles.heroOrb}>
          <div className={styles.orbOuter}>
            <div className={styles.orbMiddle}>
              <div className={styles.orbCore}>
                <BrainCircuit size={48} />
                <strong>APEXIVEAI</strong>
                <small>ENTERPRISE INTELLIGENCE</small>
              </div>
            </div>
          </div>
          <span className={styles.orbLabel}>TECHNOLOGY ECOSYSTEM</span>
        </div>
      </section>

      <section className={styles.introSection}>
        <div className={styles.sectionHeading}>
          <span className={styles.eyebrow}>WHO WE ARE</span>
          <h2>
            Technology built around
            <br />
            <span>real-world operations.</span>
          </h2>
        </div>
        <div className={styles.introCopy}>
          <p>
            ApexiveAI is an enterprise technology initiative focused on
            developing intelligent platforms and digital infrastructure for
            businesses, operators and institutions.
          </p>
          <p>
            Our technology ecosystem brings together network operations,
            enterprise AI, automation, data engineering and security to help
            organizations build connected, scalable and intelligent operations.
          </p>
        </div>
      </section>

      <section className={styles.photoSection}>
        <div className={styles.photoHeading}>
          <span className={styles.eyebrow}>OUR COMPANY</span>
          <h2>Technology, connected by design.</h2>
          <p>
            A unified view of the infrastructure and enterprise intelligence
            that powers the ApexiveAI ecosystem.
          </p>
        </div>

        <div className={styles.photoGrid}>
          <div className={`${styles.photoSlot} ${styles.photoLarge}`}>
            <div className={styles.photoIllustration} aria-hidden="true">
              <div className={styles.photoIllustrationOrbit} />
              <div className={styles.photoIllustrationOrbit} />
              <div className={styles.photoIllustrationCore}>
                <Network size={36} />
                <span>INFRASTRUCTURE</span>
              </div>
              <span className={styles.photoIllustrationNode}>NETWORK</span>
              <span className={styles.photoIllustrationNode}>CLOUD</span>
              <span className={styles.photoIllustrationNode}>OPERATIONS</span>
            </div>
            <div className={styles.photoOverlay}>
              <span>01 / APEXIVE INFRATECH</span>
              <strong>Connected infrastructure. Resilient operations.</strong>
            </div>
          </div>

          <div className={`${styles.photoSlot} ${styles.photoSmall}`}>
            <div className={styles.photoIllustration} aria-hidden="true">
              <div className={styles.photoIllustrationOrbit} />
              <div className={styles.photoIllustrationOrbit} />
              <div className={styles.photoIllustrationCore}>
                <BrainCircuit size={36} />
                <span>ENTERPRISE AI</span>
              </div>
              <span className={styles.photoIllustrationNode}>DATA</span>
              <span className={styles.photoIllustrationNode}>AI</span>
              <span className={styles.photoIllustrationNode}>INSIGHT</span>
            </div>
            <div className={styles.photoOverlay}>
              <span>02 / APEXIVE DATACRAFT</span>
              <strong>Meaningful data. Intelligent outcomes.</strong>
            </div>
          </div>
        </div>
      </section>

      <section className={styles.valuesSection}>
        <div className={styles.sectionHeading}>
          <span className={styles.eyebrow}>OUR DIRECTION</span>
          <h2>Purpose that drives innovation.</h2>
        </div>
        <div className={styles.valuesGrid}>
          <article className={styles.valueCard}>
            <div><Eye size={23} /></div>
            <span>01 / VISION</span>
            <h3>Our Vision</h3>
            <p>
              To contribute to a future where intelligent technology enables
              organizations and industries to operate with greater
              connectivity, efficiency and insight.
            </p>
          </article>
          <article className={styles.valueCard}>
            <div><Target size={23} /></div>
            <span>02 / MISSION</span>
            <h3>Our Mission</h3>
            <p>
              To engineer practical enterprise platforms that bring together
              AI, automation, infrastructure and data to address complex
              operational challenges.
            </p>
          </article>
          <article className={styles.valueCard}>
            <div><Lightbulb size={23} /></div>
            <span>03 / PRINCIPLES</span>
            <h3>Our Values</h3>
            <p>
              Innovation, engineering excellence, responsible technology,
              customer-focused solutions and continuous improvement.
            </p>
          </article>
        </div>
      </section>

      <section className={styles.divisionSection}>
        <div className={styles.divisionIntro}>
          <span className={styles.eyebrow}>OUR TECHNOLOGY ECOSYSTEM</span>
          <h2>
            Two divisions.
            <br />
            <span>One connected vision.</span>
          </h2>
          <p>
            Our portfolio is organized around infrastructure intelligence
            and enterprise data technologies.
          </p>
        </div>

        <div className={styles.divisionBlock}>
          <div className={styles.divisionHeader}>
            <div className={styles.divisionSymbol}><Network size={25} /></div>
            <div>
              <span>DIVISION 01 / CLOUD & NETWORK INFRASTRUCTURE</span>
              <h3>Apexive InfraTech</h3>
              <p>
                Modules designed for network operations and service assurance
                across telecommunications operators, internet service
                providers and cloud infrastructure environments.
              </p>
            </div>
          </div>
          <div className={styles.productsGrid}>
            {infraProducts.map((product) => (
              <ProductCard key={product.name} product={product} />
            ))}
          </div>
        </div>

        <div className={styles.divisionBlock}>
          <div className={styles.divisionHeader}>
            <div className={styles.divisionSymbol}><BrainCircuit size={25} /></div>
            <div>
              <span>DIVISION 02 / DATA & ENTERPRISE AI PLATFORM</span>
              <h3>Apexive DataCraft</h3>
              <p>
                Enterprise AI platforms, localized communication technologies,
                data infrastructure, digital twins and security solutions.
              </p>
            </div>
          </div>
          <div className={styles.productsGrid}>
            {dataProducts.map((product) => (
              <ProductCard key={product.name} product={product} />
            ))}
          </div>
        </div>
      </section>

      <section className={styles.closingSection}>
        <div>
          <span className={styles.eyebrow}>LET&apos;S BUILD WHAT&apos;S NEXT</span>
          <h2>
            Transform possibilities
            <br />
            <span>into intelligent outcomes.</span>
          </h2>
          <p>
            Explore how ApexiveAI can support your organization&apos;s technology
            and operational goals.
          </p>
        </div>
        <Link href="/contact" className={styles.primaryButton}>
          Contact ApexiveAI <ArrowUpRight size={17} />
        </Link>
      </section>
    </div>
  );
}
