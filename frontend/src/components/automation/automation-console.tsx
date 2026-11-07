"use client";

import {
  Activity,
  AlertTriangle,
  ArrowUpRight,
  BarChart3,
  Bot,
  CalendarClock,
  CheckCircle2,
  ChevronRight,
  CircleHelp,
  ClipboardList,
  Clock3,
  FileClock,
  GitBranch,
  LayoutDashboard,
  KeyRound,
  LockKeyhole,
  Network,
  Play,
  RefreshCw,
  Settings2,
  ShieldCheck,
  Workflow,
} from "lucide-react";
import Link from "next/link";
import { useCallback, useMemo, useState } from "react";
import styles from "./automation-console.module.css";

type ModuleId =
  | "overview"
  | "designer"
  | "workflows"
  | "bots"
  | "execution"
  | "queues"
  | "schedules"
  | "triggers"
  | "approvals"
  | "monitoring"
  | "history"
  | "exceptions"
  | "integrations"
  | "templates"
  | "analytics"
  | "settings"
  | "governance"
  | "credentials";

type ModuleItem = {
  id: ModuleId;
  label: string;
  endpoint?: string;
  icon: typeof Activity;
  description: string;
};

type ApiRecord = Record<string, unknown>;

function isApiRecord(value: unknown): value is ApiRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

const modules: ModuleItem[] = [
  { id: "overview", label: "Overview", icon: LayoutDashboard, description: "A live view of workflows, bots and work in progress." },
  { id: "designer", label: "Process Designer", icon: Workflow, description: "Compose governed automation from reusable workflow steps." },
  { id: "workflows", label: "Workflow Management", endpoint: "workflows", icon: GitBranch, description: "Review workflow definitions, versions and lifecycle status." },
  { id: "bots", label: "Bot Management", endpoint: "bots", icon: Bot, description: "Manage registered workers and their operational state." },
  { id: "execution", label: "Bot Execution", endpoint: "executions", icon: Play, description: "Inspect execution activity and controlled run requests." },
  { id: "queues", label: "Task Queue", endpoint: "queues", icon: ClipboardList, description: "Track queued work, priority and retry state." },
  { id: "schedules", label: "Schedules", endpoint: "schedules", icon: CalendarClock, description: "Review scheduled workflow runs." },
  { id: "triggers", label: "Triggers", endpoint: "triggers", icon: Activity, description: "Manage approved event-driven workflow triggers." },
  { id: "approvals", label: "Approvals", endpoint: "approvals", icon: CheckCircle2, description: "Review pending human decisions and approval history." },
  { id: "monitoring", label: "Live Monitoring", endpoint: "monitoring", icon: Activity, description: "Observe current bot health and execution status." },
  { id: "history", label: "Execution History", endpoint: "executions", icon: FileClock, description: "Search completed and in-progress workflow runs." },
  { id: "exceptions", label: "Exception Center", endpoint: "exceptions", icon: AlertTriangle, description: "Review failed tasks and recovery information." },
  { id: "integrations", label: "Integrations", endpoint: "integrations", icon: Network, description: "Review registered enterprise connector capabilities." },
  { id: "templates", label: "Templates", endpoint: "templates", icon: ClipboardList, description: "Start from reusable, governed workflow templates." },
  { id: "analytics", label: "Analytics & Reports", endpoint: "analytics", icon: BarChart3, description: "Explore execution trends and automation outcomes." },
  { id: "settings", label: "Settings", endpoint: "settings", icon: Settings2, description: "Configure tenant execution and worker limits." },
  { id: "governance", label: "Security & Governance", endpoint: "governance", icon: ShieldCheck, description: "Tenant policies, roles, credentials and audit trail." },
  { id: "credentials", label: "Credential Vault", endpoint: "credentials", icon: KeyRound, description: "Manage encrypted tenant credentials and approved references." },
];

const apiBase =
  process.env.NEXT_PUBLIC_AEOP_API_URL?.replace(/\/+$/, "") ??
  "http://localhost:8010";

function getArrayPayload(payload: unknown): ApiRecord[] {
  if (Array.isArray(payload)) {
    return payload.filter(
      (item): item is ApiRecord =>
        typeof item === "object" && item !== null && !Array.isArray(item),
    );
  }

  if (typeof payload === "object" && payload !== null) {
    const records = Object.values(payload).find(Array.isArray);
    if (records) {
      return records.filter(
        (item): item is ApiRecord =>
          typeof item === "object" && item !== null && !Array.isArray(item),
      );
    }
  }

  return [];
}

function readableValue(value: unknown): string {
  if (typeof value === "string" || typeof value === "number") {
    return String(value);
  }
  if (typeof value === "boolean") {
    return value ? "Enabled" : "Disabled";
  }
  return "";
}

function displayLabel(value: string): string {
  return value
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .toLowerCase()
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export default function AutomationConsole() {
  const [activeModule, setActiveModule] = useState<ModuleId>("overview");
  const [tokenInput, setTokenInput] = useState("");
  const [accessToken, setAccessToken] = useState("");
  const [overview, setOverview] = useState<ApiRecord | null>(null);
  const [records, setRecords] = useState<ApiRecord[]>([]);
  const [sectionData, setSectionData] = useState<ApiRecord | null>(null);
  const [workflowOptions, setWorkflowOptions] = useState<ApiRecord[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [workflowName, setWorkflowName] = useState("");
  const [workflowDescription, setWorkflowDescription] = useState("");
  const [workflowNeedsApproval, setWorkflowNeedsApproval] = useState(false);
  const [workflowSteps, setWorkflowSteps] = useState<ApiRecord[]>([]);
  const [workflowComponents, setWorkflowComponents] = useState<Record<string, ApiRecord[]>>({});
  const [nodeType, setNodeType] = useState("set_variable");
  const [nodeParameter, setNodeParameter] = useState("");
  const [nodeValue, setNodeValue] = useState("");
  const [savedWorkflowId, setSavedWorkflowId] = useState("");
  const [componentName, setComponentName] = useState("");
  const [componentMessage, setComponentMessage] = useState("");
  const [botName, setBotName] = useState("");
  const [credentialName, setCredentialName] = useState("");
  const [credentialSecret, setCredentialSecret] = useState("");
  const [scheduleWorkflowId, setScheduleWorkflowId] = useState("");
  const [scheduleName, setScheduleName] = useState("");
  const [cronExpression, setCronExpression] = useState("0 9 * * 1-5");
  const [triggerWorkflowId, setTriggerWorkflowId] = useState("");
  const [triggerName, setTriggerName] = useState("");
  const [triggerEvent, setTriggerEvent] = useState("");
  const [integrationName, setIntegrationName] = useState("");
  const [integrationHost, setIntegrationHost] = useState("");
  const [integrationType, setIntegrationType] = useState("REST_API");
  const [templateName, setTemplateName] = useState("");
  const [policyBots, setPolicyBots] = useState("20");
  const [policyConcurrent, setPolicyConcurrent] = useState("5");
  const [policyDaily, setPolicyDaily] = useState("1000");

  const selectedModule = useMemo(
    () => modules.find((module) => module.id === activeModule) ?? modules[0],
    [activeModule],
  );

  const fetchApi = useCallback(
    async (
      path: string,
      token: string,
      options: RequestInit = {},
    ): Promise<unknown> => {
      const headers = new Headers(options.headers);
      headers.set("Authorization", `Bearer ${token}`);
      if (options.body) {
        headers.set("Content-Type", "application/json");
      }
      const response = await fetch(`${apiBase}/api/v1/automation/${path}`, {
        ...options,
        headers,
        cache: "no-store",
      });
      const payload: unknown = await response.json();
      if (!response.ok) {
        const detail =
          typeof payload === "object" && payload !== null && "detail" in payload
            ? readableValue(payload.detail)
            : "";
        throw new Error(detail || `Automation API request failed (${response.status}).`);
      }
      return payload;
    },
    [],
  );

  const loadSection = useCallback(
    async (moduleId: ModuleId, token: string) => {
      const sectionItem = modules.find((item) => item.id === moduleId);
      if (!sectionItem?.endpoint) {
        return;
      }

      setIsLoading(true);
      setError("");
      try {
        const payload = await fetchApi(sectionItem.endpoint, token);
        setSectionData(
          typeof payload === "object" && payload !== null && !Array.isArray(payload)
            ? payload as ApiRecord
            : null,
        );
        if (
          moduleId === "settings" &&
          isApiRecord(payload) &&
          isApiRecord(payload.policy)
        ) {
          setPolicyBots(readableValue(payload.policy.max_bots) || "20");
          setPolicyConcurrent(readableValue(payload.policy.max_concurrent_executions) || "5");
          setPolicyDaily(readableValue(payload.policy.max_executions_per_day) || "1000");
        }
        const items = getArrayPayload(payload);
        setRecords(items);
        if (moduleId === "workflows") {
          setWorkflowOptions(items);
        }
      } catch (requestError) {
        setError(
          requestError instanceof Error
            ? requestError.message
            : "Unable to load automation data.",
        );
        setRecords([]);
        setSectionData(null);
      } finally {
        setIsLoading(false);
      }
    },
    [fetchApi],
  );

  async function connectWorkspace(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const token = tokenInput.trim();
    if (!token) {
      setError("Enter a valid ApexiveAI access token to connect this workspace.");
      return;
    }

    setIsLoading(true);
    setError("");
    try {
      const result = await fetchApi("overview", token);
      if (typeof result !== "object" || result === null || Array.isArray(result)) {
        throw new Error("The automation overview response is not in the expected format.");
      }
      setOverview(result as ApiRecord);
      setAccessToken(token);
      setTokenInput("");
      const workflows = await fetchApi("workflows", token);
      setWorkflowOptions(getArrayPayload(workflows));
      if (activeModule !== "overview") {
        await loadSection(activeModule, token);
      }
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to connect to the automation workspace.",
      );
      setOverview(null);
      setAccessToken("");
    } finally {
      setIsLoading(false);
    }
  }

  function selectModule(moduleId: ModuleId) {
    setActiveModule(moduleId);
    setError("");
    setNotice("");
    if (accessToken && moduleId !== "overview") {
      void loadSection(moduleId, accessToken);
    }
    if (accessToken && (moduleId === "schedules" || moduleId === "triggers")) {
      void fetchApi("workflows", accessToken)
        .then((payload) => setWorkflowOptions(getArrayPayload(payload)))
        .catch((requestError: unknown) => {
          setError(
            requestError instanceof Error
              ? requestError.message
              : "Unable to load workflow choices.",
          );
        });
    }
  }

  async function refreshCurrentSection() {
    if (activeModule === "overview" && accessToken) {
      setIsLoading(true);
      setError("");
      try {
        const result = await fetchApi("overview", accessToken);
        if (typeof result !== "object" || result === null || Array.isArray(result)) {
          throw new Error("The automation overview response is not in the expected format.");
        }
        setOverview(result as ApiRecord);
      } catch (requestError) {
        setError(
          requestError instanceof Error
            ? requestError.message
            : "Unable to refresh the automation overview.",
        );
      } finally {
        setIsLoading(false);
      }
      return;
    }
    if (accessToken) {
      await loadSection(activeModule, accessToken);
    }
  }

  async function mutateApi(
    path: string,
    method: "POST" | "PATCH" | "PUT",
    body: unknown,
    successMessage: string,
  ): Promise<unknown | null> {
    if (!accessToken) {
      setError("Connect to your workspace before making changes.");
      return null;
    }

    setIsLoading(true);
    setError("");
    setNotice("");
    try {
      const result = await fetchApi(path, accessToken, {
        method,
        ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
      });
      setNotice(successMessage);
      if (selectedModule.endpoint) {
        await loadSection(activeModule, accessToken);
      }
      return result;
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "The requested automation change failed.",
      );
      return null;
    } finally {
      setIsLoading(false);
    }
  }

  function addWorkflowStep(action = nodeType, dropped = false) {
    const stepNumber = workflowSteps.length + 1;
    const parameter = dropped
      ? action === "set_variable"
        ? `variable_${stepNumber}`
        : action === "for_each"
          ? "items"
          : `variable_${Math.max(1, stepNumber - 1)}`
      : nodeParameter.trim();
    const value = dropped ? "New workflow step" : nodeValue;
    if (action === "set_variable" && !parameter) {
      setError("Set-variable steps need a variable name.");
      return;
    }
    if (action === "log" && !value.trim()) {
      setError("Log steps need a message.");
      return;
    }
    if (action === "component" && !workflowComponents[parameter]) {
      setError("Add a reusable component before referencing it in a workflow.");
      return;
    }
    const newStep: ApiRecord =
      action === "set_variable"
        ? { type: action, key: parameter, value }
        : action === "condition"
          ? {
              type: action,
              variable: parameter,
              equals: value,
              then: [],
              else: [],
            }
          : action === "for_each"
            ? { type: action, variable: parameter, steps: [] }
            : action === "while"
              ? { type: action, variable: parameter, equals: value, steps: [] }
              : action === "parallel"
                ? { type: action, branches: [[], []] }
                : action === "component"
                  ? { type: action, name: parameter }
                  : { type: action, message: value };
    setWorkflowSteps((steps) => [...steps, newStep]);
    setNodeParameter("");
    setNodeValue("");
    setNodeType(action);
    setError("");
  }

  function dropWorkflowStep(event: React.DragEvent<HTMLDivElement>) {
    event.preventDefault();
    const action = event.dataTransfer.getData("application/x-cyclone-step");
    if (["set_variable", "condition", "for_each", "while", "parallel", "log"].includes(action)) {
      addWorkflowStep(action, true);
    }
  }

  function addReusableComponent() {
    const name = componentName.trim();
    if (!name || !componentMessage.trim()) {
      setError("Reusable components need a name and a message.");
      return;
    }
    setWorkflowComponents((components) => ({
      ...components,
      [name]: [{ type: "log", message: componentMessage.trim() }],
    }));
    setNodeType("component");
    setNodeParameter(name);
    setNodeValue("");
    setComponentName("");
    setComponentMessage("");
    setError("");
  }

  async function saveWorkflow(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const result = await mutateApi(
      "workflows",
      "POST",
      {
        name: workflowName,
        description: workflowDescription,
        requires_approval: workflowNeedsApproval,
        definition: { steps: workflowSteps, components: workflowComponents },
      },
      "Workflow saved as a draft.",
    );
    if (typeof result === "object" && result !== null && "id" in result) {
      setSavedWorkflowId(readableValue(result.id));
    }
  }

  async function publishDraft() {
    if (!savedWorkflowId) {
      setError("Save the workflow draft before publishing it.");
      return;
    }
    const result = await mutateApi(
      `workflows/${savedWorkflowId}`,
      "PATCH",
      { status: "PUBLISHED" },
      "Workflow published and ready for a worker.",
    );
    if (result) {
      setActiveModule("workflows");
      await loadSection("workflows", accessToken);
    }
  }

  async function startWorkflow(workflowId: string) {
    const result = await mutateApi(
      `workflows/${workflowId}/executions`,
      "POST",
      { input_data: {}, priority: 5 },
      "Execution request accepted. Check Task Queue for its current state.",
    );
    if (typeof result === "object" && result !== null && "id" in result) {
      setActiveModule("queues");
      await loadSection("queues", accessToken);
    }
  }

  async function registerBot(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!botName.trim()) {
      return;
    }
    const result = await mutateApi(
      "bots",
      "POST",
      { name: botName.trim(), capabilities: [] },
      "Bot registered. Start it when its worker is ready.",
    );
    if (result) {
      setBotName("");
    }
  }

  async function controlBot(botId: string, action: "START" | "STOP" | "PAUSE" | "RESUME") {
    await mutateApi(
      `bots/${botId}/control`,
      "POST",
      { action },
      `Bot ${action.toLowerCase()} requested.`,
    );
  }

  async function toggleSchedule(scheduleId: string, enabled: boolean) {
    await mutateApi(
      `schedules/${scheduleId}/toggle?enabled=${!enabled}`,
      "POST",
      undefined,
      `Schedule ${enabled ? "disabled" : "enabled"}.`,
    );
  }

  async function toggleTrigger(triggerId: string, enabled: boolean) {
    await mutateApi(
      `triggers/${triggerId}`,
      "PATCH",
      { enabled: !enabled },
      `Trigger ${enabled ? "disabled" : "enabled"}.`,
    );
  }

  async function toggleIntegration(integrationId: string, enabled: boolean) {
    await mutateApi(
      `integrations/${integrationId}/${enabled ? "disable" : "enable"}`,
      "POST",
      undefined,
      `Integration ${enabled ? "disabled" : "enabled"}.`,
    );
  }

  async function retryQueueItem(queueId: string) {
    await mutateApi(
      `queues/${queueId}/retry`,
      "POST",
      undefined,
      "A new execution has been queued for retry.",
    );
  }

  async function retryExecution(executionId: string) {
    await mutateApi(
      `executions/${executionId}/retry`,
      "POST",
      undefined,
      "A new execution has been queued for recovery.",
    );
  }

  async function instantiateTemplate(templateId: string, name: string) {
    await mutateApi(
      `templates/${templateId}/instantiate?name=${encodeURIComponent(`${name} Copy`)}`,
      "POST",
      undefined,
      "A workflow draft has been created from the template.",
    );
  }

  async function reviewApproval(approvalId: string, decision: "APPROVED" | "REJECTED") {
    await mutateApi(
      `approvals/${approvalId}/decision`,
      "POST",
      { decision },
      `Approval ${decision.toLowerCase()}.`,
    );
  }

  async function saveCredential(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const result = await mutateApi(
      "credentials",
      "POST",
      { name: credentialName.trim(), secret: credentialSecret },
      "Credential encrypted and stored. Its value will not be shown again.",
    );
    if (result) {
      setCredentialName("");
      setCredentialSecret("");
    }
  }

  async function saveSchedule(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await mutateApi(
      "schedules",
      "POST",
      {
        name: scheduleName.trim(),
        workflow_id: scheduleWorkflowId,
        cron_expression: cronExpression,
        timezone_name: "Asia/Yangon",
        enabled: true,
      },
      "Schedule created. A running CoreRPA worker will dispatch it at the next scheduled time.",
    );
  }

  async function saveTrigger(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await mutateApi(
      "triggers",
      "POST",
      {
        name: triggerName.trim(),
        workflow_id: triggerWorkflowId,
        event_name: triggerEvent.trim(),
        enabled: true,
      },
      "Trigger created and available for authenticated event dispatch.",
    );
  }

  async function saveIntegration(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await mutateApi(
      "integrations",
      "POST",
      {
        name: integrationName.trim(),
        connector_type: integrationType,
        approved_hosts: integrationHost.split(",").map((host) => host.trim()).filter(Boolean),
      },
      "Connector metadata registered. External execution adapters are not enabled by this configuration.",
    );
  }

  async function saveTemplate(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await mutateApi(
      "templates",
      "POST",
      {
        name: templateName.trim(),
        description: "Reusable starter for a governed enterprise process.",
        category: "Enterprise Operations",
        definition: { steps: workflowSteps, components: workflowComponents },
      },
      "Workflow template saved.",
    );
  }

  async function saveTenantPolicy(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await mutateApi(
      "governance/policy",
      "PUT",
      {
        max_bots: Number(policyBots),
        max_concurrent_executions: Number(policyConcurrent),
        max_executions_per_day: Number(policyDaily),
      },
      "Tenant execution policy updated.",
    );
  }

  const overviewMetrics = overview
    ? Object.entries(overview).filter(
        ([, value]) => typeof value === "number" || typeof value === "string",
      )
    : [];
  const sectionMetrics =
    sectionData && ["analytics", "monitoring", "governance"].includes(activeModule)
      ? Object.entries(sectionData).flatMap(([key, value]) => {
          if (typeof value === "number" || typeof value === "string") {
            return [[key, value] as [string, unknown]];
          }
          if (typeof value === "object" && value !== null && !Array.isArray(value)) {
            return Object.entries(value).filter(
              ([, nestedValue]) =>
                typeof nestedValue === "number" ||
                typeof nestedValue === "string" ||
                typeof nestedValue === "boolean",
            );
          }
          return [];
        })
      : [];
  const activeIcon = selectedModule.icon;
  const ActiveIcon = activeIcon;

  return (
    <div className={styles.workspace}>
      <aside className={styles.sidebar}>
        <div className={styles.sidebarBrand}>
          <span className={styles.brandMark}><Bot size={19} /></span>
          <span><strong>CYCLONE</strong><small>APEXIVEAI RPA</small></span>
        </div>
        <div className={styles.tenantLabel}>AUTOMATION WORKSPACE</div>
        <nav className={styles.moduleNav} aria-label="CoreRPA modules">
          {modules.map((module) => {
            const Icon = module.icon;
            return (
              <button
                type="button"
                key={module.id}
                className={activeModule === module.id ? styles.navActive : ""}
                onClick={() => selectModule(module.id)}
              >
                <Icon size={17} />
                <span>{module.label}</span>
                {activeModule === module.id && <ChevronRight size={14} />}
              </button>
            );
          })}
        </nav>
        <div className={styles.sidebarFooter}>
          <LockKeyhole size={15} />
          <span>Tenant-scoped · Role governed</span>
        </div>
      </aside>

      <div className={styles.main}>
        <header className={styles.topbar}>
          <div className={styles.breadcrumb}>
            <span>AEOP</span><ChevronRight size={14} /><span>Apexive CoreRPA</span>
            <ChevronRight size={14} /><strong>{selectedModule.label}</strong>
          </div>
          <div className={styles.connectionStatus}>
            <span className={accessToken ? styles.connectedDot : styles.offlineDot} />
            {accessToken ? "Workspace connected" : "Not connected"}
          </div>
        </header>

        <div className={styles.content}>
          <section className={styles.pageHeading}>
            <div>
              <span className={styles.eyebrow}>APEXIVEAI · GOVERNED AUTOMATION</span>
              <h1>{selectedModule.label}</h1>
              <p>{selectedModule.description}</p>
            </div>
            {accessToken && (
              <button
                type="button"
                className={styles.refreshButton}
                onClick={() => void refreshCurrentSection()}
                disabled={isLoading}
              >
                <RefreshCw size={16} className={isLoading ? styles.spinning : ""} />
                Refresh
              </button>
            )}
          </section>

          {!accessToken ? (
            <section className={styles.connectCard}>
              <div className={styles.connectIcon}><LockKeyhole size={22} /></div>
              <div className={styles.connectCopy}>
                <h2>Connect to your secure workspace</h2>
                <p>
                  CoreRPA data is protected by ApexiveAI identity and tenant
                  controls. Add a valid access token to load your live workspace.
                  The token stays in memory for this page session only.
                </p>
                <form className={styles.connectForm} onSubmit={connectWorkspace}>
                  <label htmlFor="automation-token">ApexiveAI access token</label>
                  <div className={styles.tokenEntry}>
                    <input
                      id="automation-token"
                      type="password"
                      autoComplete="off"
                      value={tokenInput}
                      onChange={(event) => setTokenInput(event.target.value)}
                      placeholder="Paste access token"
                    />
                    <button type="submit" disabled={isLoading || !tokenInput.trim()}>
                      {isLoading ? "Connecting..." : "Connect"}
                      <ArrowUpRight size={15} />
                    </button>
                  </div>
                </form>
              </div>
              <div className={styles.apiHint}>
                <span>API ENDPOINT</span>
                <code>{apiBase}/api/v1/automation</code>
              </div>
            </section>
          ) : activeModule === "overview" ? (
            <>
              {overviewMetrics.length > 0 ? (
                <div className={styles.metricGrid}>
                  {overviewMetrics.slice(0, 6).map(([key, value]) => (
                    <article className={styles.metricCard} key={key}>
                      <span>{displayLabel(key)}</span>
                      <strong>{readableValue(value)}</strong>
                      <small>Current tenant</small>
                    </article>
                  ))}
                </div>
              ) : (
                <section className={styles.emptyState}>
                  <Activity size={23} />
                  <strong>No overview metrics available</strong>
                  <span>The connected workspace did not return summary metrics.</span>
                </section>
              )}
              <section className={styles.overviewGrid}>
                <article className={styles.panel}>
                  <div className={styles.panelHeading}>
                    <div><span className={styles.eyebrow}>AUTOMATION LIFECYCLE</span><h2>One governed flow</h2></div>
                    <GitBranch size={19} />
                  </div>
                  <div className={styles.lifecycle}>
                    {[
                      ["01", "Design", "Versioned visual workflows"],
                      ["02", "Orchestrate", "Bots, queues and schedules"],
                      ["03", "Review", "Approvals and exception handling"],
                      ["04", "Improve", "Monitoring and analytics"],
                    ].map(([number, title, description]) => (
                      <div className={styles.lifecycleStep} key={number}>
                        <span>{number}</span><div><strong>{title}</strong><small>{description}</small></div>
                      </div>
                    ))}
                  </div>
                </article>
                <article className={styles.panel}>
                  <div className={styles.panelHeading}>
                    <div><span className={styles.eyebrow}>PLATFORM SAFEGUARDS</span><h2>Built for enterprise control</h2></div>
                    <ShieldCheck size={19} />
                  </div>
                  <ul className={styles.safeguardList}>
                    <li><CheckCircle2 size={16} /><span>Tenant-isolated workflow and execution data</span></li>
                    <li><CheckCircle2 size={16} /><span>Role-based design and operational permissions</span></li>
                    <li><CheckCircle2 size={16} /><span>Approval gates for sensitive process steps</span></li>
                    <li><CheckCircle2 size={16} /><span>Execution limits and auditable actions</span></li>
                  </ul>
                </article>
              </section>
              <p className={styles.liveDataNote}><CircleHelp size={15} /> Metrics above are fetched from the connected automation API; no sample execution data is shown.</p>
            </>
          ) : activeModule === "designer" ? (
            <div className={styles.designerLayout}>
              <section className={styles.panel}>
                <div className={styles.panelHeading}>
                  <div><span className={styles.eyebrow}>VERSIONED WORKFLOW</span><h2>Design a process</h2></div>
                  <Workflow size={19} />
                </div>
                <form className={styles.workspaceForm} onSubmit={saveWorkflow}>
                  <label className={styles.formField}>
                    Workflow name
                    <input required value={workflowName} onChange={(event) => setWorkflowName(event.target.value)} maxLength={160} />
                  </label>
                  <label className={styles.formField}>
                    Description
                    <textarea value={workflowDescription} onChange={(event) => setWorkflowDescription(event.target.value)} maxLength={1000} rows={2} />
                  </label>
                  <label className={styles.checkField}>
                    <input type="checkbox" checked={workflowNeedsApproval} onChange={(event) => setWorkflowNeedsApproval(event.target.checked)} />
                    Require independent approval before execution
                  </label>
                  <div className={styles.nodeComposer}>
                    <label className={styles.formField}>
                      Step type
                      <select value={nodeType} onChange={(event) => setNodeType(event.target.value)}>
                        <option value="set_variable">Set variable</option>
                        <option value="condition">If / Else condition</option>
                        <option value="for_each">For each item</option>
                        <option value="while">While condition</option>
                        <option value="parallel">Parallel branches</option>
                        <option value="component">Reusable component</option>
                        <option value="log">Log a message</option>
                      </select>
                    </label>
                    {nodeType !== "log" && nodeType !== "parallel" && (
                      <label className={styles.formField}>
                        {nodeType === "set_variable" ? "Variable key" : nodeType === "component" ? "Component name" : "Variable name"}
                        <input value={nodeParameter} onChange={(event) => setNodeParameter(event.target.value)} maxLength={64} />
                      </label>
                    )}
                    {nodeType !== "for_each" && nodeType !== "parallel" && nodeType !== "component" && (
                      <label className={styles.formField}>
                        {nodeType === "set_variable" ? "Value" : nodeType === "condition" ? "Equals" : "Message"}
                        <input value={nodeValue} onChange={(event) => setNodeValue(event.target.value)} maxLength={500} />
                      </label>
                    )}
                    <button className={styles.secondaryButton} type="button" onClick={() => addWorkflowStep()}>
                      Add step <Workflow size={14} />
                    </button>
                  </div>
                  <div className={styles.componentBuilder}>
                    <strong>Reusable component</strong>
                    <div>
                      <input aria-label="Reusable component name" value={componentName} onChange={(event) => setComponentName(event.target.value)} placeholder="Component name" maxLength={80} />
                      <input aria-label="Reusable component message" value={componentMessage} onChange={(event) => setComponentMessage(event.target.value)} placeholder="Reusable log message" maxLength={500} />
                      <button className={styles.secondaryButton} type="button" onClick={addReusableComponent}>Add component</button>
                    </div>
                    {Object.keys(workflowComponents).length > 0 && (
                      <small>Available: {Object.keys(workflowComponents).join(", ")}</small>
                    )}
                  </div>
                  <button className={styles.primaryButton} type="submit" disabled={isLoading || !workflowSteps.length}>
                    Save workflow draft <ArrowUpRight size={15} />
                  </button>
                </form>
                {savedWorkflowId && (
                  <div className={styles.publishBar}>
                    <span>Draft saved · {savedWorkflowId.slice(0, 8)}</span>
                    <button className={styles.primaryButton} type="button" onClick={() => void publishDraft()} disabled={isLoading}>
                      Publish workflow <ArrowUpRight size={15} />
                    </button>
                  </div>
                )}
              </section>
              <section
                className={`${styles.panel} ${styles.canvasPanel}`}
                onDragOver={(event) => event.preventDefault()}
                onDrop={dropWorkflowStep}
              >
                <div className={styles.panelHeading}>
                  <div><span className={styles.eyebrow}>VISUAL FLOW</span><h2>Workflow canvas</h2></div>
                  <span className={styles.recordCount}>{workflowSteps.length} steps</span>
                </div>
                <div className={styles.nodePalette}>
                  {["set_variable", "condition", "for_each", "while", "parallel", "log"].map((action) => (
                    <button
                      type="button"
                      draggable
                      key={action}
                      onDragStart={(event) => event.dataTransfer.setData("application/x-cyclone-step", action)}
                      onClick={() => addWorkflowStep(action, true)}
                    >
                      <Workflow size={14} /> {displayLabel(action)}
                    </button>
                  ))}
                </div>
                <div className={styles.workflowCanvas}>
                  {workflowSteps.length ? workflowSteps.map((step, index) => (
                    <article className={styles.workflowNode} key={`${readableValue(step.type)}-${index}`}>
                      <span>{String(index + 1).padStart(2, "0")}</span>
                      <div><strong>{displayLabel(readableValue(step.type))}</strong><small>{JSON.stringify(step)}</small></div>
                      <button type="button" aria-label={`Remove step ${index + 1}`} onClick={() => setWorkflowSteps((items) => items.filter((_, itemIndex) => itemIndex !== index))}>×</button>
                    </article>
                  )) : (
                    <div className={styles.canvasEmpty}><Workflow size={21} /><span>Drag a step here or use the step builder.</span></div>
                  )}
                  {workflowSteps.length > 1 && <div className={styles.flowConnector} />}
                </div>
                <p className={styles.liveDataNote}>Workflow actions are validated against the server&apos;s allow-listed runtime before they can be saved.</p>
              </section>
            </div>
          ) : (
            <>
            {activeModule === "bots" && (
              <form className={`${styles.panel} ${styles.inlineForm}`} onSubmit={registerBot}>
                <div><span className={styles.eyebrow}>WORKER REGISTRATION</span><h2>Register a bot worker</h2></div>
                <input aria-label="Bot name" required maxLength={160} value={botName} onChange={(event) => setBotName(event.target.value)} placeholder="Worker name" />
                <button className={styles.primaryButton} type="submit" disabled={isLoading}>Register bot</button>
              </form>
            )}
            {activeModule === "schedules" && (
              <form className={`${styles.panel} ${styles.formGrid}`} onSubmit={saveSchedule}>
                <div className={styles.formIntro}><span className={styles.eyebrow}>SCHEDULED AUTOMATION</span><h2>Create a schedule</h2></div>
                <label className={styles.formField}>Schedule name<input required value={scheduleName} onChange={(event) => setScheduleName(event.target.value)} maxLength={160} /></label>
                <label className={styles.formField}>Published workflow<select required value={scheduleWorkflowId} onChange={(event) => setScheduleWorkflowId(event.target.value)}><option value="">Select workflow</option>{workflowOptions.filter((workflow) => workflow.status === "PUBLISHED").map((workflow) => <option key={readableValue(workflow.id)} value={readableValue(workflow.id)}>{readableValue(workflow.name)}</option>)}</select></label>
                <label className={styles.formField}>Cron expression<input required value={cronExpression} onChange={(event) => setCronExpression(event.target.value)} placeholder="0 9 * * 1-5" /></label>
                <button className={styles.primaryButton} type="submit" disabled={isLoading}>Create schedule</button>
              </form>
            )}
            {activeModule === "triggers" && (
              <form className={`${styles.panel} ${styles.formGrid}`} onSubmit={saveTrigger}>
                <div className={styles.formIntro}><span className={styles.eyebrow}>EVENT AUTOMATION</span><h2>Create a trigger</h2></div>
                <label className={styles.formField}>Trigger name<input required value={triggerName} onChange={(event) => setTriggerName(event.target.value)} maxLength={160} /></label>
                <label className={styles.formField}>Published workflow<select required value={triggerWorkflowId} onChange={(event) => setTriggerWorkflowId(event.target.value)}><option value="">Select workflow</option>{workflowOptions.filter((workflow) => workflow.status === "PUBLISHED").map((workflow) => <option key={readableValue(workflow.id)} value={readableValue(workflow.id)}>{readableValue(workflow.name)}</option>)}</select></label>
                <label className={styles.formField}>Event name<input required value={triggerEvent} onChange={(event) => setTriggerEvent(event.target.value)} maxLength={120} placeholder="e.g. invoice.received" /></label>
                <button className={styles.primaryButton} type="submit" disabled={isLoading}>Create trigger</button>
              </form>
            )}
            {activeModule === "integrations" && (
              <form className={`${styles.panel} ${styles.formGrid}`} onSubmit={saveIntegration}>
                <div className={styles.formIntro}><span className={styles.eyebrow}>REGISTERED CONNECTORS</span><h2>Register an integration</h2></div>
                <label className={styles.formField}>Integration name<input required value={integrationName} onChange={(event) => setIntegrationName(event.target.value)} maxLength={160} /></label>
                <label className={styles.formField}>Connector type<select value={integrationType} onChange={(event) => setIntegrationType(event.target.value)}>{["REST_API", "BROWSER", "DATABASE", "FILES", "DOCUMENTS", "DESKTOP", "EMAIL"].map((type) => <option key={type}>{type}</option>)}</select></label>
                <label className={styles.formField}>Approved hostnames (comma separated)<input value={integrationHost} onChange={(event) => setIntegrationHost(event.target.value)} placeholder="api.example.com" /></label>
                <button className={styles.primaryButton} type="submit" disabled={isLoading}>Register metadata</button>
              </form>
            )}
            {activeModule === "templates" && (
              <form className={`${styles.panel} ${styles.inlineForm}`} onSubmit={saveTemplate}>
                <div><span className={styles.eyebrow}>REUSABLE PROCESSES</span><h2>Create a template from the current canvas</h2></div>
                <input aria-label="Template name" required value={templateName} onChange={(event) => setTemplateName(event.target.value)} placeholder="Template name" maxLength={160} />
                <button className={styles.primaryButton} type="submit" disabled={isLoading}>Save template</button>
              </form>
            )}
            {activeModule === "credentials" && (
              <form className={`${styles.panel} ${styles.formGrid}`} onSubmit={saveCredential}>
                <div className={styles.formIntro}><span className={styles.eyebrow}>ENCRYPTED TENANT VAULT</span><h2>Add a credential</h2></div>
                <label className={styles.formField}>Credential name<input required value={credentialName} onChange={(event) => setCredentialName(event.target.value)} maxLength={160} /></label>
                <label className={styles.formField}>Secret value<input type="password" autoComplete="new-password" required value={credentialSecret} onChange={(event) => setCredentialSecret(event.target.value)} maxLength={8000} /></label>
                <button className={styles.primaryButton} type="submit" disabled={isLoading}>Encrypt and save</button>
                <p className={styles.liveDataNote}>Secrets are encrypted at rest and are never included in API responses. Configure the vault encryption key on the backend first.</p>
              </form>
            )}
            {activeModule === "settings" && (
              <form className={`${styles.panel} ${styles.formGrid}`} onSubmit={saveTenantPolicy}>
                <div className={styles.formIntro}><span className={styles.eyebrow}>TENANT EXECUTION POLICY</span><h2>Set resource limits</h2></div>
                <label className={styles.formField}>Maximum bots<input type="number" min={0} max={500} required value={policyBots} onChange={(event) => setPolicyBots(event.target.value)} /></label>
                <label className={styles.formField}>Concurrent runs<input type="number" min={1} max={100} required value={policyConcurrent} onChange={(event) => setPolicyConcurrent(event.target.value)} /></label>
                <label className={styles.formField}>Daily execution requests<input type="number" min={1} max={100000} required value={policyDaily} onChange={(event) => setPolicyDaily(event.target.value)} /></label>
                <button className={styles.primaryButton} type="submit" disabled={isLoading}>Save limits</button>
                <p className={styles.liveDataNote}>Only tenant administrators can change limits. The backend enforces these values before queueing work.</p>
              </form>
            )}
            {sectionMetrics.length > 0 && (
              <div className={styles.metricGrid}>
                {sectionMetrics.slice(0, 6).map(([key, value]) => (
                  <article className={styles.metricCard} key={key}>
                    <span>{displayLabel(key)}</span>
                    <strong>{readableValue(value)}</strong>
                    <small>Current tenant</small>
                  </article>
                ))}
              </div>
            )}
            <section className={styles.panel}>
              <div className={styles.panelHeading}>
                <div>
                  <span className={styles.eyebrow}>TENANT WORKSPACE DATA</span>
                  <h2>{selectedModule.label}</h2>
                </div>
                <span className={styles.recordCount}>
                  {isLoading ? "Loading" : `${records.length} records`}
                </span>
              </div>
              {error ? (
                <div className={styles.errorState}><AlertTriangle size={17} /><span>{error}</span></div>
              ) : isLoading ? (
                <div className={styles.emptyState}><Clock3 size={22} /><strong>Loading workspace data</strong><span>Retrieving the latest tenant-scoped records.</span></div>
              ) : records.length > 0 ? (
                <div className={styles.recordList}>
                  {records.map((record, index) => {
                    const title =
                      readableValue(record.name) ||
                      readableValue(record.title) ||
                      readableValue(record.workflow_name) ||
                      readableValue(record.execution_id) ||
                      readableValue(record.id) ||
                      `Record ${index + 1}`;
                    const status =
                      (readableValue(record.status) ||
                      readableValue(record.state) ||
                      (typeof record.enabled === "boolean"
                        ? record.enabled
                          ? "ENABLED"
                          : "DISABLED"
                        : "AVAILABLE")).toUpperCase();
                    const detail =
                      readableValue(record.description) ||
                      readableValue(record.message) ||
                      readableValue(record.connector_type) ||
                      readableValue(record.cron_expression) ||
                      readableValue(record.error_message) ||
                      readableValue(record.workflow_id) ||
                      readableValue(record.created_at);
                    return (
                      <article className={styles.recordRow} key={readableValue(record.id) || `${title}-${index}`}>
                        <div className={styles.recordIcon}><ActiveIcon size={17} /></div>
                        <div className={styles.recordCopy}><strong>{title}</strong><small>{detail || "Tenant workspace resource"}</small></div>
                        <span className={styles.statusPill}>{displayLabel(status)}</span>
                        {activeModule === "workflows" && status === "DRAFT" && (
                          <button className={styles.rowAction} type="button" onClick={() => void mutateApi(`workflows/${readableValue(record.id)}`, "PATCH", { status: "PUBLISHED" }, "Workflow published.")}>Publish</button>
                        )}
                        {activeModule === "workflows" && status === "PUBLISHED" && (
                          <button className={styles.rowAction} type="button" onClick={() => void startWorkflow(readableValue(record.id))}>Queue run</button>
                        )}
                        {activeModule === "bots" && (
                          <div className={styles.rowActions}>
                            {status === "OFFLINE" && <button className={styles.rowAction} type="button" onClick={() => void controlBot(readableValue(record.id), "START")}>Start</button>}
                            {status === "IDLE" && <button className={styles.rowAction} type="button" onClick={() => void controlBot(readableValue(record.id), "PAUSE")}>Pause</button>}
                            {status === "PAUSED" && <button className={styles.rowAction} type="button" onClick={() => void controlBot(readableValue(record.id), "RESUME")}>Resume</button>}
                            {(status === "IDLE" || status === "PAUSED") && <button className={styles.rowAction} type="button" onClick={() => void controlBot(readableValue(record.id), "STOP")}>Stop</button>}
                          </div>
                        )}
                        {activeModule === "approvals" && status === "PENDING" && (
                          <div className={styles.rowActions}>
                            <button className={styles.rowAction} type="button" onClick={() => void reviewApproval(readableValue(record.id), "APPROVED")}>Approve</button>
                            <button className={styles.rowAction} type="button" onClick={() => void reviewApproval(readableValue(record.id), "REJECTED")}>Reject</button>
                          </div>
                        )}
                        {activeModule === "schedules" && (
                          <div className={styles.rowActions}>
                            <button className={styles.rowAction} type="button" onClick={() => void toggleSchedule(readableValue(record.id), record.enabled === true)}>{record.enabled === true ? "Disable" : "Enable"}</button>
                            <button className={styles.rowAction} type="button" onClick={() => void mutateApi(`schedules/${readableValue(record.id)}/run`, "POST", undefined, "Scheduled workflow queued.")}>Run now</button>
                          </div>
                        )}
                        {activeModule === "triggers" && (
                          <button className={styles.rowAction} type="button" onClick={() => void toggleTrigger(readableValue(record.id), record.enabled === true)}>{record.enabled === true ? "Disable" : "Enable"}</button>
                        )}
                        {activeModule === "integrations" && (
                          <button className={styles.rowAction} type="button" onClick={() => void toggleIntegration(readableValue(record.id), record.enabled === true)}>{record.enabled === true ? "Disable" : "Enable"}</button>
                        )}
                        {activeModule === "queues" && status === "DEAD" && (
                          <button className={styles.rowAction} type="button" onClick={() => void retryQueueItem(readableValue(record.id))}>Retry</button>
                        )}
                        {activeModule === "exceptions" && status === "FAILED" && (
                          <button className={styles.rowAction} type="button" onClick={() => void retryExecution(readableValue(record.id))}>Recover</button>
                        )}
                        {activeModule === "templates" && (
                          <button className={styles.rowAction} type="button" onClick={() => void instantiateTemplate(readableValue(record.id), readableValue(record.name) || "Workflow")}>Create workflow</button>
                        )}
                      </article>
                    );
                  })}
                </div>
              ) : (
                <div className={styles.emptyState}>
                  <selectedModule.icon size={23} />
                  <strong>No {selectedModule.label.toLowerCase()} found</strong>
                  <span>There are no records available for the connected tenant.</span>
                </div>
              )}
            </section>
            </>
          )}

          {error && !accessToken && <div className={styles.errorState}><AlertTriangle size={17} /><span>{error}</span></div>}
          {notice && <div className={styles.successState}><CheckCircle2 size={16} /><span>{notice}</span></div>}

          <footer className={styles.pageFooter}>
            <span><LockKeyhole size={14} /> ApexiveAI CoreRPA · Governed automation workspace</span>
            <Link href="/products/apexive-cyclone-rpa">Product overview <ArrowUpRight size={14} /></Link>
          </footer>
        </div>
      </div>
    </div>
  );
}
