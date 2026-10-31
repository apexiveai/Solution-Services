import Link from "next/link";
import {
  RadioTower,
  Mail,
  Route,
  Landmark,
  Wallet,
  Zap,
  Factory,
  ArrowUpRight,
} from "lucide-react";

const industries = [
  {
    number: "01",
    title: "Telecom Industry",
    description:
      "Intelligent telecom operations, network automation and service intelligence.",
    href: "/solutions/telecom",
    icon: RadioTower,
  },
  {
    number: "02",
    title: "Postal Industry",
    description:
      "Digital postal operations, intelligent sorting and delivery management.",
    href: "/solutions/postal",
    icon: Mail,
  },
  {
    number: "03",
    title: "Transportation Industry",
    description:
      "Connected transportation, highway intelligence and mobility operations.",
    href: "/solutions/transportation",
    icon: Route,
  },
  {
    number: "04",
    title: "Public Services",
    description:
      "Digital government, public services and smart city operations.",
    href: "/solutions/public-services",
    icon: Landmark,
  },
  {
    number: "05",
    title: "Finance Industry",
    description:
      "Enterprise financial operations, analytics and intelligent automation.",
    href: "/solutions/finance",
    icon: Wallet,
  },
  {
    number: "06",
    title: "Energy Industry",
    description:
      "Energy infrastructure intelligence and operational monitoring.",
    href: "/solutions/energy",
    icon: Zap,
  },
  {
    number: "07",
    title: "Manufacturing Industry",
    description:
      "Industry 4.0, smart factories and industrial data intelligence.",
    href: "/solutions/manufacturing",
    icon: Factory,
  },
];

export default function IndustrySection() {
  return (
    <section className="industry-section" id="industries">
      <div className="section-container">
        <div className="section-heading">
          <div>
            <span className="eyebrow">INDUSTRY EXPERTISE</span>
            <h2>
              Technology built around
              <br />
              <span>your industry.</span>
            </h2>
          </div>

          <div className="section-heading-side">
            <p>
              Purpose-built enterprise solutions that connect people,
              processes, data and technology across critical industries.
            </p>

            <Link href="/solutions" className="text-link">
              View all industries <ArrowUpRight size={17} />
            </Link>
          </div>
        </div>

        <div className="industry-grid">
          {industries.map((industry) => {
            const Icon = industry.icon;

            return (
              <Link
                href={industry.href}
                className="industry-card"
                key={industry.number}
              >
                <div className="industry-card-top">
                  <span className="industry-number">{industry.number}</span>
                  <span className="industry-icon">
                    <Icon size={23} strokeWidth={1.7} />
                  </span>
                </div>

                <div className="industry-card-body">
                  <h3>{industry.title}</h3>
                  <p>{industry.description}</p>
                </div>

                <div className="industry-card-bottom">
                  <span>Explore solution</span>
                  <ArrowUpRight size={18} />
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </section>
  );
}