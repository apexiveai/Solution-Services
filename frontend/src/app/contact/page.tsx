
import Link from "next/link";
import {
  ArrowRight,
  ArrowUpRight,
  Mail,
  MapPin,
  MessageSquare,
  Building2,
  Globe2,
  Clock3,
} from "lucide-react";
import styles from "./contact.module.css";

export const metadata = {
  title: "Contact ApexiveAI | Enterprise Technology & Solutions",
  description:
    "Contact ApexiveAI for enterprise technology, telecom infrastructure, AI platforms, partnerships and business inquiries.",
};

const inquiryTypes = [
  "General Business Inquiry",
  "Cloud & Network Infrastructure",
  "Enterprise AI & Data Platform",
  "Software & Professional Services",
  "Partnership & Collaboration",
  "Other",
];

export default function ContactPage() {
  return (
    <div className={styles.contactPage}>
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <span className={styles.eyebrow}>CONTACT APEXIVEAI</span>
          <h1>
            Let&apos;s start a
            <br />
            <span>conversation.</span>
          </h1>
          <p>
            Have a project, business inquiry or partnership opportunity?
            Connect with our team and explore what&apos;s possible.
          </p>
          <div className={styles.heroTag}>
            <MessageSquare size={17} />
            ENTERPRISE TECHNOLOGY / BUSINESS INQUIRIES
          </div>
        </div>
        <div className={styles.heroVisual}>
          <div className={styles.visualCircle}>
            <div className={styles.visualCore}>
              <Globe2 size={44} />
              <strong>CONNECT</strong>
              <small>WITH APEXIVEAI</small>
            </div>
          </div>
          <span className={styles.visualLabel}>INTELLIGENCE IN MOTION.</span>
        </div>
      </section>

      <section className={styles.contactContent}>
        <div className={styles.contactInfo}>
          <span className={styles.eyebrow}>GET IN TOUCH</span>
          <h2>We&apos;d like to hear from you.</h2>
          <p className={styles.infoIntro}>
            Reach out to discuss enterprise solutions, technology services
            and potential business collaborations.
          </p>

          <div className={styles.infoCard}>
            <div className={styles.infoIcon}><Mail size={21} /></div>
            <div>
              <span>BUSINESS EMAIL</span>
              <strong>Official email to be confirmed</strong>
              <small>Replace with your verified company email.</small>
            </div>
          </div>

          <div className={styles.infoCard}>
            <div className={styles.infoIcon}><MapPin size={21} /></div>
            <div>
              <span>OFFICE LOCATION</span>
              <strong>Myanmar</strong>
              <small>Official office address to be published.</small>
            </div>
          </div>

          <div className={styles.infoCard}>
            <div className={styles.infoIcon}><Building2 size={21} /></div>
            <div>
              <span>BUSINESS & PARTNERSHIPS</span>
              <strong>Enterprise Solutions</strong>
              <small>Technology projects, integration and collaboration.</small>
            </div>
          </div>

          <div className={styles.infoCard}>
            <div className={styles.infoIcon}><Clock3 size={21} /></div>
            <div>
              <span>INQUIRY SUPPORT</span>
              <strong>Business inquiries</strong>
              <small>Contact us with your requirements and objectives.</small>
            </div>
          </div>
        </div>

        <div className={styles.formCard}>
          <div className={styles.formHeading}>
            <span className={styles.eyebrow}>SEND AN INQUIRY</span>
            <h2>How can we help?</h2>
            <p>Share a few details about your inquiry.</p>
          </div>

          <form className={styles.form}>
            <div className={styles.fieldRow}>
              <label>
                Full Name <span>*</span>
                <input name="name" type="text" placeholder="Your full name" required />
              </label>
              <label>
                Company
                <input name="company" type="text" placeholder="Company name" />
              </label>
            </div>

            <div className={styles.fieldRow}>
              <label>
                Business Email <span>*</span>
                <input name="email" type="email" placeholder="name@company.com" required />
              </label>
              <label>
                Phone Number
                <input name="phone" type="tel" placeholder="+95 ..." />
              </label>
            </div>

            <label>
              Inquiry Type <span>*</span>
              <select name="inquiryType" defaultValue="" required>
                <option value="" disabled>Select an inquiry category</option>
                {inquiryTypes.map((type) => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </label>

            <label>
              Subject
              <input name="subject" type="text" placeholder="How can we assist?" />
            </label>

            <label>
              Message <span>*</span>
              <textarea
                name="message"
                rows={5}
                placeholder="Tell us about your project, requirements or business inquiry..."
                required
              />
            </label>

            <button className={styles.submitButton} type="button" disabled>
              Inquiry submission coming soon
              <ArrowRight size={17} />
            </button>
            <p className={styles.formNote}>
              The inquiry form interface is prepared. Submission will be
              activated after the secure backend and company email are
              configured.
            </p>
          </form>
        </div>
      </section>

      <section className={styles.bottomCta}>
        <div>
          <span className={styles.eyebrow}>EXPLORE OUR ECOSYSTEM</span>
          <h2>Discover what we can build together.</h2>
        </div>
        <Link href="/about" className={styles.secondaryButton}>
          About ApexiveAI <ArrowUpRight size={17} />
        </Link>
      </section>
    </div>
  );
}
