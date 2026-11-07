"use client";

import { ArrowRight, BadgeCheck, Building2, CreditCard, KeyRound, RefreshCw, ShieldCheck } from "lucide-react";
import Link from "next/link";
import { useState, type FormEvent } from "react";
import styles from "./core-rpa-licensing-console.module.css";

type RecordValue = Record<string, unknown>;

const apiBase =
  process.env.NEXT_PUBLIC_AEOP_API_URL?.replace(/\/+$/, "") ??
  "http://localhost:8010";

const serviceOptions = [
  ["ENTERPRISE_PROCESS_ASSESSMENT", "Enterprise Process Assessment"],
  ["PROOF_OF_CONCEPT", "Proof of Concept (PoC)"],
  ["ENTERPRISE_QUOTATION", "Enterprise Quotation"],
  ["LICENSING_DEPLOYMENT", "Licensing & Deployment"],
  ["CUSTOM_BOT_DEVELOPMENT", "Custom Bot Development"],
  ["TRAINING_ANNUAL_SUPPORT", "Training & Annual Support"],
];

function isRecord(value: unknown): value is RecordValue {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function text(value: unknown): string {
  return typeof value === "string" || typeof value === "number" ? String(value) : "";
}

function formatCurrency(amount: unknown, currency: unknown): string {
  if (amount === null || amount === undefined || amount === "") return "Awaiting quotation";
  const value = Number(amount);
  if (!Number.isFinite(value)) return "Awaiting quotation";
  return `${text(currency) || "MMK"} ${value.toLocaleString()}`;
}

export default function CoreRpaLicensingConsole() {
  const [tokenInput, setTokenInput] = useState("");
  const [token, setToken] = useState("");
  const [opportunities, setOpportunities] = useState<RecordValue[]>([]);
  const [orders, setOrders] = useState<RecordValue[]>([]);
  const [licenses, setLicenses] = useState<RecordValue[]>([]);
  const [developerSeats, setDeveloperSeats] = useState<RecordValue[]>([]);
  const [usage, setUsage] = useState<RecordValue | null>(null);
  const [requestKind, setRequestKind] = useState("LICENSE");
  const [serviceType, setServiceType] = useState("ENTERPRISE_PROCESS_ASSESSMENT");
  const [departments, setDepartments] = useState("Finance, HR, IT, Procurement");
  const [developers, setDevelopers] = useState("5");
  const [bots, setBots] = useState("10");
  const [term, setTerm] = useState("12");
  const [deployment, setDeployment] = useState("PRIVATE_CLOUD");
  const [requirements, setRequirements] = useState("");
  const [quoteAmount, setQuoteAmount] = useState("");
  const [quoteCurrency, setQuoteCurrency] = useState("MMK");
  const [quoteExpiry, setQuoteExpiry] = useState("");
  const [quoteNotes, setQuoteNotes] = useState("");
  const [paymentReference, setPaymentReference] = useState("");
  const [developerSubject, setDeveloperSubject] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function api(path: string, method = "GET", body?: RecordValue): Promise<unknown> {
    const response = await fetch(`${apiBase}/api/v1/core-rpa/${path}`, {
      method,
      headers: {
        Authorization: `Bearer ${token}`,
        ...(body ? { "Content-Type": "application/json" } : {}),
      },
      ...(body ? { body: JSON.stringify(body) } : {}),
      cache: "no-store",
    });
    const responseText = await response.text();
    const payload: unknown = responseText ? JSON.parse(responseText) : null;
    if (!response.ok) {
      const detail = isRecord(payload) ? text(payload.detail) : "";
      throw new Error(detail || `Request failed (${response.status})`);
    }
    return payload;
  }

  async function refresh(nextToken = token) {
    setToken(nextToken);
    const paths = ["opportunities", "orders", "licenses", "usage", "developers"];
    const [opportunityData, orderData, licenseData, usageData, seatData] = await Promise.all(
      paths.map(async (path) => {
        const response = await fetch(`${apiBase}/api/v1/core-rpa/${path}`, {
          headers: { Authorization: `Bearer ${nextToken}` },
          cache: "no-store",
        });
        const responseText = await response.text();
        const payload: unknown = responseText ? JSON.parse(responseText) : null;
        if (!response.ok) {
          const detail = isRecord(payload) ? text(payload.detail) : "";
          throw new Error(detail || `Could not load ${path} (${response.status})`);
        }
        return payload;
      }),
    );
    setOpportunities(Array.isArray(opportunityData) ? opportunityData.filter(isRecord) : []);
    setOrders(Array.isArray(orderData) ? orderData.filter(isRecord) : []);
    setLicenses(Array.isArray(licenseData) ? licenseData.filter(isRecord) : []);
    setUsage(isRecord(usageData) ? usageData : null);
    setDeveloperSeats(Array.isArray(seatData) ? seatData.filter(isRecord) : []);
  }

  async function perform(action: () => Promise<unknown>, success: string) {
    setBusy(true);
    setError("");
    setMessage("");
    try {
      await action();
      await refresh();
      setMessage(success);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "The request could not be completed.");
    } finally {
      setBusy(false);
    }
  }

  function submitOpportunity(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void perform(
      () =>
        api("opportunities", "POST", {
          request_kind: requestKind,
          service_type: requestKind === "SERVICE" ? serviceType : "CORE_RPA_LICENSE",
          departments: departments.split(",").map((item) => item.trim()).filter(Boolean),
          requested_developers: Number(developers),
          requested_bots: Number(bots),
          term_months: Number(term),
          deployment,
          requirements,
        }),
      "Your assessment or license quotation request has been submitted.",
    );
  }

  function setQuotation(opportunity: RecordValue, status: string) {
    const expiry = quoteExpiry ? new Date(quoteExpiry).toISOString() : null;
    void perform(
      () =>
        api(`opportunities/${text(opportunity.id)}/quotation`, "PATCH", {
          status,
          quote_amount: quoteAmount ? Number(quoteAmount) : null,
          currency: quoteCurrency,
          quote_valid_until: expiry,
          quote_notes: quoteNotes || null,
          approved_developers: Number(developers),
          approved_bots: Number(bots),
          approved_monthly_executions: Math.max(Number(bots) * 100, 1000),
          term_months: Number(term),
        }),
      `Opportunity moved to ${status.toLowerCase()}.`,
    );
  }

  function requestOrder(opportunity: RecordValue) {
    void perform(
      () => api(`opportunities/${text(opportunity.id)}/orders`, "POST"),
      "The order is ready for agreement and invoice payment.",
    );
  }

  function acceptAgreement(order: RecordValue) {
    void perform(
      () =>
        api(`orders/${text(order.id)}/agreement`, "POST", {
          accepted: true,
          agreement_reference: `AEOP-CORE-RPA-${text(order.order_number)}`,
        }),
      "Agreement accepted. Submit your invoice payment reference next.",
    );
  }

  function submitPayment(order: RecordValue) {
    void perform(
      () =>
        api(`orders/${text(order.id)}/payment`, "POST", {
          payment_reference: paymentReference,
        }),
      "Payment reference submitted for manual verification.",
    );
  }

  function decidePayment(order: RecordValue, verified: boolean) {
    void perform(
      () =>
        api(`orders/${text(order.id)}/payment-decision`, "POST", {
          verified,
          notes: verified ? "Manual invoice payment confirmed." : "Payment not confirmed.",
        }),
      verified ? "Payment verified and tenant license activated." : "Payment returned for review.",
    );
  }

  function prepareRenewals() {
    void perform(
      () => api("renewals/prepare?within_days=30", "POST"),
      "Renewal quotations prepared for licenses approaching expiry.",
    );
  }

  function assignDeveloper() {
    void perform(
      () => api("developers", "POST", { subject: developerSubject }),
      "Developer seat assigned.",
    );
    setDeveloperSubject("");
  }

  function revokeDeveloperSeat(seat: RecordValue) {
    void perform(
      () => api(`developers/${text(seat.id)}`, "DELETE"),
      "Developer seat revoked.",
    );
  }

  return (
    <main className={styles.page}>
      <section className={styles.hero}>
        <div className={styles.heroGlow} />
        <div className={styles.heroInner}>
          <Link className={styles.backLink} href="/products/apexive-cyclone-rpa">← Apexive CoreRPA</Link>
          <span className={styles.eyebrow}>INTELLIGENCE IN MOTION</span>
          <h1>Enterprise services.<br /><span>Licensed automation.</span></h1>
          <p>
            Assess your processes, validate a PoC, receive an enterprise quotation,
            sign the license agreement and activate CoreRPA in your tenant.
          </p>
          <div className={styles.flow}>
            {["Assessment", "Quotation", "Agreement", "Payment", "Activation", "Renewal"].map((item, index) => (
              <span key={item}><i>0{index + 1}</i>{item}</span>
            ))}
          </div>
        </div>
      </section>

      <section className={styles.content}>
        <div className={styles.connectCard}>
          <div>
            <span className={styles.eyebrow}>SECURE TENANT ACCESS</span>
            <h2>Connect to your ApexiveAI account</h2>
            <p>Use your signed-in access token to create requests and manage your tenant licenses.</p>
          </div>
          <form
            className={styles.tokenForm}
            onSubmit={(event) => {
              event.preventDefault();
              setBusy(true);
              setError("");
              void refresh(tokenInput.trim())
                .then(() => setMessage("Tenant licensing data loaded."))
                .catch((requestError: unknown) =>
                  setError(requestError instanceof Error ? requestError.message : "Could not load account data."),
                )
                .finally(() => setBusy(false));
            }}
          >
            <input
              aria-label="ApexiveAI access token"
              type="password"
              autoComplete="off"
              placeholder="Paste access token"
              value={tokenInput}
              onChange={(event) => setTokenInput(event.target.value)}
              required
            />
            <button type="submit" disabled={busy || !tokenInput.trim()}>
              {busy ? "Connecting…" : "Connect"}
              <ArrowRight size={16} />
            </button>
          </form>
        </div>

        {(error || message) && (
          <p className={error ? styles.error : styles.notice} role="status">{error || message}</p>
        )}

        {token && (
          <>
            <section className={styles.usageGrid}>
              <article><span>LICENSE STATUS</span><strong>{text(usage?.license && isRecord(usage.license) ? usage.license.status : "No active license")}</strong><small>{usage?.license && isRecord(usage.license) ? `Expires ${new Date(text(usage.license.expires_at)).toLocaleDateString()}` : "Request a quotation to get started"}</small></article>
              <article><span>BOT CAPACITY</span><strong>{text(usage?.bots_used)} / {text(usage?.bots_limit)}</strong><small>Registered CoreRPA bots</small></article>
              <article><span>MONTHLY EXECUTIONS</span><strong>{text(usage?.executions_this_month)} / {text(usage?.executions_limit)}</strong><small>Usage for the current month</small></article>
              <article><span>DEVELOPER SEATS</span><strong>{text(usage?.developers_used)} / {text(usage?.developers_limit)}</strong><small>Assigned tenant users</small></article>
            </section>

            <div className={styles.sectionHeading}>
              <div><span className={styles.eyebrow}>ASSESSMENT & SALES</span><h2>Start your enterprise journey</h2></div>
              <span className={styles.secureLabel}><ShieldCheck size={16} /> Tenant-scoped and auditable</span>
            </div>

            <div className={styles.columns}>
              <form className={styles.formCard} onSubmit={submitOpportunity}>
                <h3><Building2 size={18} /> Request a service or license</h3>
                <label>Request type
                  <select value={requestKind} onChange={(event) => setRequestKind(event.target.value)}>
                    <option value="LICENSE">CoreRPA software license</option>
                    <option value="SERVICE">ApexiveAI professional service</option>
                  </select>
                </label>
                {requestKind === "SERVICE" && (
                  <label>Service
                    <select value={serviceType} onChange={(event) => setServiceType(event.target.value)}>
                      {serviceOptions.map(([value, label]) => <option value={value} key={value}>{label}</option>)}
                    </select>
                  </label>
                )}
                <label>Departments
                  <input value={departments} onChange={(event) => setDepartments(event.target.value)} placeholder="Finance, HR, IT" />
                </label>
                <div className={styles.formRow}>
                  <label>Developers<input type="number" min="1" value={developers} onChange={(event) => setDevelopers(event.target.value)} /></label>
                  <label>Robots<input type="number" min="1" value={bots} onChange={(event) => setBots(event.target.value)} /></label>
                </div>
                <div className={styles.formRow}>
                  <label>License term
                    <select value={term} onChange={(event) => setTerm(event.target.value)}>
                      <option value="12">12 months</option><option value="24">24 months</option><option value="36">36 months</option>
                    </select>
                  </label>
                  <label>Deployment
                    <select value={deployment} onChange={(event) => setDeployment(event.target.value)}>
                      <option value="AEOP_CLOUD">AEOP Cloud</option><option value="PRIVATE_CLOUD">Private cloud</option><option value="ON_PREMISES">On premises</option><option value="HYBRID">Hybrid</option>
                    </select>
                  </label>
                </div>
                <label>Requirements<textarea value={requirements} onChange={(event) => setRequirements(event.target.value)} rows={4} placeholder="Processes, systems, PoC goals or deployment needs" /></label>
                <button className={styles.primaryButton} type="submit" disabled={busy}>Submit request <ArrowRight size={16} /></button>
              </form>

              <div className={styles.formCard}>
                <h3><KeyRound size={18} /> License and developer seats</h3>
                <p className={styles.helper}>Licenses activate only after agreement acceptance and manual invoice payment verification.</p>
                <div className={styles.seatForm}>
                  <input value={developerSubject} onChange={(event) => setDeveloperSubject(event.target.value)} placeholder="User subject / identity ID" />
                  <button type="button" onClick={assignDeveloper} disabled={busy || !developerSubject.trim()}>Assign seat</button>
                </div>
                <div className={styles.seatList}>
                  {developerSeats.map((seat) => (
                    <div key={text(seat.id)}>
                      <span>{text(seat.subject)}</span>
                      <button type="button" onClick={() => revokeDeveloperSeat(seat)} disabled={busy}>Revoke</button>
                    </div>
                  ))}
                  {developerSeats.length === 0 && <small>No developer seats assigned.</small>}
                </div>
                <button className={styles.secondaryButton} type="button" onClick={prepareRenewals} disabled={busy}>
                  <RefreshCw size={15} /> Prepare due renewal quotations
                </button>
                <div className={styles.renewalNotice}>
                  <BadgeCheck size={17} />
                  <span>{usage?.renewal_due ? "Your license is within its renewal window." : "License validity and usage are checked against your tenant."}</span>
                </div>
              </div>
            </div>

            <section className={styles.listSection}>
              <div className={styles.sectionHeading}><div><span className={styles.eyebrow}>QUOTE PIPELINE</span><h2>Assessments & quotations</h2></div></div>
              {opportunities.length === 0 ? <p className={styles.empty}>No requests yet. Submit a service or license request to begin.</p> : opportunities.map((opportunity) => (
                <article className={styles.listCard} key={text(opportunity.id)}>
                  <div className={styles.listMain}>
                    <div><strong>{text(opportunity.service_type).replaceAll("_", " ")}</strong><span>{text(opportunity.request_kind)} · {text(opportunity.status)}</span></div>
                    <strong>{formatCurrency(opportunity.quote_amount, opportunity.currency)}</strong>
                  </div>
                  <p>{text(opportunity.quote_notes) || text(opportunity.requirements) || "No additional notes."}</p>
                  {opportunity.request_kind !== "SERVICE" && opportunity.status === "QUOTED" && (
                    <button className={styles.primaryButton} type="button" onClick={() => requestOrder(opportunity)} disabled={busy}>
                      Place software order <ArrowRight size={15} />
                    </button>
                  )}
                  {opportunity.status !== "ACCEPTED" && opportunity.status !== "DECLINED" && opportunity.status !== "COMPLETED" && (
                    <details className={styles.salesControls}>
                      <summary>Sales team · update assessment / quotation</summary>
                      <div className={styles.formRow}>
                        <label>Stage<select id={`stage-${text(opportunity.id)}`} defaultValue={text(opportunity.status) === "SUBMITTED" ? "ASSESSMENT" : text(opportunity.status)}><option value="ASSESSMENT">Assessment</option><option value="POC">PoC</option><option value="QUOTED">Quoted</option><option value="DECLINED">Declined</option><option value="COMPLETED">Completed</option></select></label>
                        <label>Quote amount<input id={`amount-${text(opportunity.id)}`} type="number" min="0" step="0.01" value={quoteAmount} onChange={(event) => setQuoteAmount(event.target.value)} /></label>
                      </div>
                      <div className={styles.formRow}>
                        <label>Currency<input value={quoteCurrency} maxLength={3} onChange={(event) => setQuoteCurrency(event.target.value.toUpperCase())} /></label>
                        <label>Valid until<input type="date" value={quoteExpiry} onChange={(event) => setQuoteExpiry(event.target.value)} /></label>
                      </div>
                      <label>Quotation notes<input value={quoteNotes} onChange={(event) => setQuoteNotes(event.target.value)} /></label>
                      <button className={styles.secondaryButton} type="button" disabled={busy} onClick={() => {
                        const selected = document.getElementById(`stage-${text(opportunity.id)}`) as HTMLSelectElement | null;
                        setQuotation(opportunity, selected?.value || "ASSESSMENT");
                      }}>Save opportunity stage</button>
                    </details>
                  )}
                </article>
              ))}
            </section>

            <section className={styles.listSection}>
              <div className={styles.sectionHeading}><div><span className={styles.eyebrow}>ORDER TO ACTIVATION</span><h2>Orders & payment status</h2></div></div>
              {orders.length === 0 ? <p className={styles.empty}>No software orders are waiting for action.</p> : orders.map((order) => (
                <article className={styles.listCard} key={text(order.id)}>
                  <div className={styles.listMain}><div><strong>{text(order.order_number)}</strong><span>{text(order.status)} · {text(order.plan_code)} · {text(order.term_months)} months</span></div><strong>{formatCurrency(order.amount, order.currency)}</strong></div>
                  <p>{text(order.deployment)} · {text(order.developer_limit)} developer seats · {text(order.bot_limit)} robots</p>
                  {order.status === "AGREEMENT_REQUIRED" && <><p className={styles.agreementNotice}>By accepting, your tenant records agreement to this quoted plan, term, deployment, developer and bot limits. Keep the order number with your signed contract.</p><button className={styles.primaryButton} type="button" onClick={() => acceptAgreement(order)} disabled={busy}>Accept license agreement <ArrowRight size={15} /></button></>}
                  {order.status === "PAYMENT_DUE" && <div className={styles.seatForm}><input value={paymentReference} onChange={(event) => setPaymentReference(event.target.value)} placeholder="Bank transfer / invoice payment reference" /><button type="button" onClick={() => submitPayment(order)} disabled={busy || paymentReference.length < 3}>Submit payment reference</button></div>}
                  {order.status === "PAYMENT_REVIEW" && <div className={styles.reviewActions}><span>Manual payment verification pending</span><button type="button" onClick={() => decidePayment(order, true)} disabled={busy}>Verify & activate</button><button type="button" onClick={() => decidePayment(order, false)} disabled={busy}>Reject payment</button></div>}
                </article>
              ))}
            </section>

            <section className={styles.listSection}>
              <div className={styles.sectionHeading}><div><span className={styles.eyebrow}>ACCOUNT AUTHORIZATION</span><h2>Tenant licenses</h2></div></div>
              {licenses.length === 0 ? <p className={styles.empty}>No CoreRPA account license has been activated.</p> : licenses.map((license) => (
                <article className={styles.listCard} key={text(license.id)}>
                  <div className={styles.listMain}><div><strong>{text(license.plan_code)} · {text(license.status)}</strong><span>Valid until {new Date(text(license.expires_at)).toLocaleDateString()}</span></div><button className={styles.secondaryButton} type="button" onClick={() => void perform(() => api(`licenses/${text(license.id)}/renewal`, "POST"), "Renewal request submitted.")} disabled={busy}>Request renewal</button></div>
                </article>
              ))}
            </section>
          </>
        )}

        <div className={styles.paymentInfo}><CreditCard size={18} /><span>Payments use an invoice / bank transfer workflow. A CoreRPA tenant license is provisioned only after a sales administrator verifies the payment.</span></div>
      </section>
    </main>
  );
}
