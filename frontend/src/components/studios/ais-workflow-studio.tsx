"use client";

import {
  Activity,
  ArrowDown,
  ArrowUp,
  Bot,
  Braces,
  Check,
  ChevronDown,
  CircleHelp,
  Clock3,
  Code2,
  Download,
  FileJson2,
  Layers3,
  Monitor,
  MousePointer2,
  Package,
  Play,
  Plus,
  Save,
  ScreenShare,
  Settings2,
  ShieldCheck,
  Sparkles,
  Square,
  Trash2,
  Upload,
  Workflow,
  X,
} from "lucide-react";
import Image from "next/image";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import styles from "./ais-workflow-studio.module.css";

type StepType = "set_variable" | "prompt";
type WorkflowStep = {
  id: string;
  type: StepType;
  key: string;
  value: string;
  prompt: string;
};
type RuntimeView = "designer" | "testing" | "runtime" | "publish";
type ApiRecord = Record<string, unknown>;
type WorkflowRecord = ApiRecord & {
  id: string;
  name: string;
  status: string;
  definition: ApiRecord;
};
type ExecutionRecord = ApiRecord & {
  id: string;
  workflow_id: string;
  status: string;
  error_message?: string | null;
};

const apiBase =
  process.env.NEXT_PUBLIC_AEOP_API_URL?.replace(/\/+$/, "") ??
  "http://localhost:8010";
const storageKey = "apexive-ais-studio-draft-v1";

const initialSteps: WorkflowStep[] = [
  {
    id: "step-input",
    type: "set_variable",
    key: "text",
    value: '"Add representative input before running."',
    prompt: "",
  },
  {
    id: "step-summary",
    type: "prompt",
    key: "summary",
    value: "",
    prompt: "Summarize the following text: {{text}}",
  },
];

const runtimeViews: { id: RuntimeView; label: string; icon: typeof Workflow }[] = [
  { id: "designer", label: "Designer", icon: Workflow },
  { id: "testing", label: "Test & debug", icon: Activity },
  { id: "runtime", label: "Runtime", icon: Settings2 },
  { id: "publish", label: "Publish", icon: Upload },
];

const starterInput = JSON.stringify(
  { text: "ApexiveAI Studio workflow test input." },
  null,
  2,
);

function isRecord(value: unknown): value is ApiRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function getRecords(value: unknown): ApiRecord[] {
  if (Array.isArray(value)) return value.filter(isRecord);
  if (isRecord(value) && Array.isArray(value.items)) {
    return value.items.filter(isRecord);
  }
  return [];
}

function readError(error: unknown): string {
  return error instanceof Error ? error.message : "The request could not be completed.";
}

function toWorkflowDefinition(steps: WorkflowStep[]) {
  return {
    runtime: "AIS",
    contract_version: 1,
    steps: steps.map((step) =>
      step.type === "set_variable"
        ? {
            type: step.type,
            key: step.key.trim(),
            value: JSON.parse(step.value) as unknown,
          }
        : {
            type: step.type,
            key: step.key.trim(),
            prompt: step.prompt,
          },
    ),
  };
}

function formatStep(step: WorkflowStep): string {
  return step.type === "prompt" ? "AI prompt" : "Set variable";
}

function safeFilename(value: string): string {
  return value.trim().replace(/[^a-z0-9-_]+/gi, "-").replace(/^-+|-+$/g, "") || "ais-workflow";
}

export default function AisWorkflowStudio() {
  const [view, setView] = useState<RuntimeView>("designer");
  const [workflowName, setWorkflowName] = useState("New AIS workflow");
  const [steps, setSteps] = useState<WorkflowStep[]>(initialSteps);
  const [selectedStepId, setSelectedStepId] = useState(initialSteps[1].id);
  const [inputText, setInputText] = useState(starterInput);
  const [token, setToken] = useState("");
  const [workflows, setWorkflows] = useState<WorkflowRecord[]>([]);
  const [executions, setExecutions] = useState<ExecutionRecord[]>([]);
  const [selectedWorkflowId, setSelectedWorkflowId] = useState("");
  const [requiresApproval, setRequiresApproval] = useState(true);
  const [runtimeModel, setRuntimeModel] = useState("Apexive AI");
  const [runtimeEndpoint, setRuntimeEndpoint] = useState("");
  const [runtimeTimeout, setRuntimeTimeout] = useState("120");
  const [debugLines, setDebugLines] = useState<string[]>([
    "Ready. Add an activity or validate the current workflow.",
  ]);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [isBusy, setIsBusy] = useState(false);
  const [hasLoadedDraft, setHasLoadedDraft] = useState(false);
  const [screenStream, setScreenStream] = useState<MediaStream | null>(null);
  const [screenImage, setScreenImage] = useState("");
  const [selectorOpen, setSelectorOpen] = useState(false);
  const [selectorValue, setSelectorValue] = useState("");
  const [browserRecorderOpen, setBrowserRecorderOpen] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  const selectedStep = steps.find((step) => step.id === selectedStepId) ?? null;
  const publishedWorkflows = workflows.filter((workflow) => workflow.status === "PUBLISHED");
  const draftWorkflows = workflows.filter((workflow) => workflow.status === "DRAFT");
  const activeExecutionCount = executions.filter((execution) =>
    ["QUEUED", "PENDING_APPROVAL", "RUNNING"].includes(execution.status),
  ).length;

  useEffect(() => {
    let active = true;
    queueMicrotask(() => {
      if (!active) return;
      try {
        const saved = window.localStorage.getItem(storageKey);
        if (saved) {
          const draft: unknown = JSON.parse(saved);
          if (isRecord(draft)) {
            if (typeof draft.workflowName === "string") setWorkflowName(draft.workflowName);
            if (Array.isArray(draft.steps)) {
              const validSteps = draft.steps.filter(
                (step): step is WorkflowStep =>
                  isRecord(step)
                  && typeof step.id === "string"
                  && (step.type === "set_variable" || step.type === "prompt")
                  && typeof step.key === "string"
                  && typeof step.value === "string"
                  && typeof step.prompt === "string",
              );
              setSteps(validSteps);
              setSelectedStepId(validSteps[0]?.id ?? "");
            }
            if (typeof draft.inputText === "string") setInputText(draft.inputText);
            if (typeof draft.runtimeModel === "string") setRuntimeModel(draft.runtimeModel);
            if (typeof draft.runtimeEndpoint === "string") setRuntimeEndpoint(draft.runtimeEndpoint);
            if (typeof draft.runtimeTimeout === "string") setRuntimeTimeout(draft.runtimeTimeout);
          }
        }
      } catch (storageError) {
        setError(`Could not restore the local AIS draft: ${readError(storageError)}`);
      } finally {
        setHasLoadedDraft(true);
      }
    });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!hasLoadedDraft) return;
    try {
      window.localStorage.setItem(
        storageKey,
        JSON.stringify({ workflowName, steps, inputText, runtimeModel, runtimeEndpoint, runtimeTimeout }),
      );
    } catch (storageError) {
      queueMicrotask(() => setError(`Could not save the local AIS draft: ${readError(storageError)}`));
    }
  }, [hasLoadedDraft, inputText, runtimeEndpoint, runtimeModel, runtimeTimeout, steps, workflowName]);

  useEffect(() => {
    if (videoRef.current && screenStream) {
      videoRef.current.srcObject = screenStream;
    }
  }, [screenStream]);

  useEffect(
    () => () => {
      screenStream?.getTracks().forEach((track) => track.stop());
    },
    [screenStream],
  );

  const request = useCallback(
    async (path: string, accessToken: string, options: RequestInit = {}): Promise<unknown> => {
      const headers = new Headers(options.headers);
      headers.set("Authorization", `Bearer ${accessToken}`);
      if (options.body) headers.set("Content-Type", "application/json");
      const response = await fetch(`${apiBase}/api/v1/automation/${path}`, {
        ...options,
        headers,
        cache: "no-store",
      });
      const text = await response.text();
      let payload: unknown = null;
      if (text) {
        try {
          payload = JSON.parse(text) as unknown;
        } catch {
          throw new Error("The CoreRPA API returned an invalid response.");
        }
      }
      if (!response.ok) {
        throw new Error(
          isRecord(payload) && typeof payload.detail === "string"
            ? payload.detail
            : `CoreRPA API request failed (${response.status}).`,
        );
      }
      return payload;
    },
    [],
  );

  const loadData = useCallback(async () => {
    if (!token.trim()) {
      setError("Enter an orchestrator access token to connect.");
      return;
    }
    setIsBusy(true);
    setError("");
    setNotice("");
    try {
      const [workflowPayload, executionPayload] = await Promise.all([
        request("workflows?limit=100", token.trim()),
        request("executions?limit=100", token.trim()),
      ]);
      const matchingWorkflows = getRecords(workflowPayload)
        .filter((record) => isRecord(record.definition) && record.definition.runtime === "AIS")
        .filter(
          (record): record is WorkflowRecord =>
            typeof record.id === "string"
            && typeof record.name === "string"
            && typeof record.status === "string"
            && isRecord(record.definition),
        );
      const matchingExecutions = getRecords(executionPayload)
        .filter((record) => typeof record.workflow_id === "string")
        .filter((record) => matchingWorkflows.some((workflow) => workflow.id === record.workflow_id))
        .filter(
          (record): record is ExecutionRecord =>
            typeof record.id === "string"
            && typeof record.workflow_id === "string"
            && typeof record.status === "string",
        );
      setWorkflows(matchingWorkflows);
      setExecutions(matchingExecutions);
      setSelectedWorkflowId((current) =>
        matchingWorkflows.some((workflow) => workflow.id === current)
          ? current
          : matchingWorkflows.find((workflow) => workflow.status === "PUBLISHED")?.id
            ?? matchingWorkflows[0]?.id
            ?? "",
      );
      setNotice(`Connected. ${matchingWorkflows.length} AIS workflows loaded.`);
    } catch (requestError) {
      setError(readError(requestError));
    } finally {
      setIsBusy(false);
    }
  }, [request, token]);

  function addStep(type: StepType) {
    const newStep: WorkflowStep = {
      id: `step-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
      type,
      key: type === "prompt" ? "ai_result" : "new_variable",
      value: '""',
      prompt: "Write a concise response about {{text}}.",
    };
    setSteps((current) => [...current, newStep]);
    setSelectedStepId(newStep.id);
    setView("designer");
    setError("");
  }

  function updateStep(id: string, updates: Partial<WorkflowStep>) {
    setSteps((current) => current.map((step) => (step.id === id ? { ...step, ...updates } : step)));
  }

  function deleteStep(id: string) {
    const index = steps.findIndex((step) => step.id === id);
    const remaining = steps.filter((step) => step.id !== id);
    setSteps(remaining);
    setSelectedStepId(remaining[Math.max(0, index - 1)]?.id ?? "");
  }

  function moveStep(id: string, offset: -1 | 1) {
    setSteps((current) => {
      const index = current.findIndex((step) => step.id === id);
      const target = index + offset;
      if (index < 0 || target < 0 || target >= current.length) return current;
      const next = [...current];
      [next[index], next[target]] = [next[target], next[index]];
      return next;
    });
  }

  const validateWorkflow = useCallback(() => {
    setError("");
    setNotice("");
    const lines: string[] = [];
    if (!workflowName.trim()) {
      setError("Give this workflow a name before testing.");
      return false;
    }
    if (steps.length > 200) {
      setError("AIS workflows are limited to 200 activities.");
      return false;
    }
    let definition: ReturnType<typeof toWorkflowDefinition>;
    let input: unknown;
    try {
      definition = toWorkflowDefinition(steps);
      input = JSON.parse(inputText);
      if (!isRecord(input)) throw new Error("Test input must be a JSON object.");
    } catch (validationError) {
      setError(readError(validationError));
      return false;
    }

    const availableKeys = new Set(Object.keys(input));
    for (const [index, step] of steps.entries()) {
      if (!/^[A-Za-z0-9_]{1,64}$/.test(step.key.trim())) {
        setError(`Activity ${index + 1} has an invalid output key. Use 1-64 letters, numbers or underscores.`);
        return false;
      }
      if (step.type === "set_variable") {
        try {
          JSON.parse(step.value);
        } catch {
          setError(`Set Variable activity ${index + 1} must contain a valid JSON value.`);
          return false;
        }
        availableKeys.add(step.key.trim());
        lines.push(`Activity ${index + 1}: set "${step.key.trim()}" locally.`);
        continue;
      }
      if (!step.prompt.trim() || step.prompt.length > 8000) {
        setError(`AI Prompt activity ${index + 1} must contain 1-8,000 characters.`);
        return false;
      }
      const placeholders = [...step.prompt.matchAll(/{{(.*?)}}/g)].map((match) => match[1].trim());
      const malformed = step.prompt.includes("{{") && /{{[^}]*$/.test(step.prompt);
      if (malformed) {
        setError(`AI Prompt activity ${index + 1} has an unclosed variable placeholder.`);
        return false;
      }
      const missing = placeholders.find(
        (key) => !/^[A-Za-z0-9_]{1,64}$/.test(key) || !availableKeys.has(key),
      );
      if (missing) {
        setError(`AI Prompt activity ${index + 1} references an unavailable input or earlier output: "${missing}".`);
        return false;
      }
      availableKeys.add(step.key.trim());
      lines.push(`Activity ${index + 1}: AI prompt is valid; model calls are not made by local dry-run.`);
    }

    setDebugLines([
      `Local dry-run validation passed · ${definition.steps.length} activities`,
      ...lines,
      "No AI model or desktop/browser action was executed. Use an approved runtime to run the workflow.",
    ]);
    setNotice("Local dry-run passed. No external model or desktop actions were executed.");
    return true;
  }, [inputText, steps, workflowName]);

  async function saveWorkflow(publish = false) {
    if (!token.trim()) {
      setError("Connect an orchestrator access token before saving or publishing.");
      setView("publish");
      return;
    }
    setIsBusy(true);
    setError("");
    setNotice("");
    try {
      const definition = toWorkflowDefinition(steps);
      const existing = workflows.find((workflow) => workflow.id === selectedWorkflowId);
      const workflowPayload = {
        name: workflowName.trim(),
        description: "Created in ApexiveAI AIS Studio",
        definition,
        requires_approval: requiresApproval,
      };
      const saved = await request(
        existing ? `workflows/${existing.id}` : "workflows",
        token.trim(),
        {
          method: existing ? "PATCH" : "POST",
          body: JSON.stringify(workflowPayload),
        },
      );
      if (!isRecord(saved) || typeof saved.id !== "string") {
        throw new Error("The orchestrator did not return the saved workflow.");
      }
      setSelectedWorkflowId(saved.id);
      if (publish) {
        await request(`workflows/${saved.id}`, token.trim(), {
          method: "PATCH",
          body: JSON.stringify({ status: "PUBLISHED" }),
        });
      }
      setNotice(publish
        ? "Workflow published to the CoreRPA orchestrator."
        : "Workflow saved as a draft in the CoreRPA orchestrator.");
      await loadData();
    } catch (saveError) {
      setError(readError(saveError));
    } finally {
      setIsBusy(false);
    }
  }

  async function runWorkflow() {
    if (!validateWorkflow()) {
      setView("testing");
      return;
    }
    if (!token.trim()) {
      setError("Connect to the orchestrator to request a licensed runtime execution.");
      setView("publish");
      return;
    }
    let inputData: unknown;
    try {
      inputData = JSON.parse(inputText);
    } catch (inputError) {
      setError(readError(inputError));
      setView("testing");
      return;
    }
    if (!isRecord(inputData)) {
      setError("Execution input must be a JSON object.");
      setView("testing");
      return;
    }
    setIsBusy(true);
    setError("");
    setNotice("");
    try {
      const selected = workflows.find((workflow) => workflow.id === selectedWorkflowId);
      const saved = await request(
        selected ? `workflows/${selected.id}` : "workflows",
        token.trim(),
        {
          method: selected ? "PATCH" : "POST",
          body: JSON.stringify({
            name: workflowName.trim(),
            description: "Created in ApexiveAI AIS Studio",
            definition: toWorkflowDefinition(steps),
            requires_approval: requiresApproval,
          }),
        },
      );
      if (!isRecord(saved) || typeof saved.id !== "string") {
        throw new Error("The orchestrator did not return the saved workflow.");
      }
      const workflowId = saved.id;
      if (saved.status !== "PUBLISHED") {
        await request(`workflows/${workflowId}`, token.trim(), {
          method: "PATCH",
          body: JSON.stringify({ status: "PUBLISHED" }),
        });
      }
      setSelectedWorkflowId(workflowId);
      await request(`workflows/${workflowId}/executions`, token.trim(), {
        method: "POST",
        body: JSON.stringify({ input_data: inputData, priority: 5 }),
      });
      setNotice("Execution request queued for an active, licensed CoreRPA worker.");
      await loadData();
    } catch (runError) {
      setError(readError(runError));
    } finally {
      setIsBusy(false);
    }
  }

  function downloadPackage() {
    try {
      const definition = toWorkflowDefinition(steps);
      const pack = {
        package_format: "apexive-ais-workflow",
        package_version: 1,
        name: workflowName.trim(),
        created_at: new Date().toISOString(),
        definition,
        runtime_configuration: {
          model: runtimeModel,
          timeout_seconds: Number(runtimeTimeout),
        },
      };
      const url = URL.createObjectURL(
        new Blob([JSON.stringify(pack, null, 2)], { type: "application/json" }),
      );
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `${safeFilename(workflowName)}.ais.json`;
      anchor.click();
      URL.revokeObjectURL(url);
      setNotice("Workflow package downloaded as a portable JSON file.");
      setError("");
    } catch (packageError) {
      setError(readError(packageError));
    }
  }

  async function startScreenCapture() {
    if (!navigator.mediaDevices?.getDisplayMedia) {
      setError("Screen capture is not supported in this browser or page context.");
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({ video: true, audio: false });
      stream.getVideoTracks()[0]?.addEventListener("ended", () => setScreenStream(null), { once: true });
      setScreenStream(stream);
      setScreenImage("");
      setNotice("Screen share connected. Choose Capture frame to save a still image.");
      setError("");
    } catch (captureError) {
      setError(readError(captureError));
    }
  }

  function captureFrame() {
    const video = videoRef.current;
    if (!video || video.readyState < HTMLMediaElement.HAVE_CURRENT_DATA) {
      setError("Wait for the shared screen preview to be ready, then capture again.");
      return;
    }
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d")?.drawImage(video, 0, 0);
    setScreenImage(canvas.toDataURL("image/png"));
    setNotice("Screen frame captured in this page session.");
    setError("");
  }

  function stopScreenCapture() {
    screenStream?.getTracks().forEach((track) => track.stop());
    setScreenStream(null);
  }

  async function copySelector() {
    if (!selectorValue.trim()) {
      setError("Enter a CSS or accessible-name selector first.");
      return;
    }
    try {
      await navigator.clipboard.writeText(selectorValue.trim());
      setNotice("Selector copied. Browser/desktop interaction activities require a connected recorder agent.");
      setError("");
    } catch (clipboardError) {
      setError(`Could not copy the selector: ${readError(clipboardError)}`);
    }
  }

  const selectedWorkflow = useMemo(
    () => workflows.find((workflow) => workflow.id === selectedWorkflowId) ?? null,
    [selectedWorkflowId, workflows],
  );

  return (
    <main className={styles.studio}>
      <header className={styles.topbar}>
        <div className={styles.brand}>
          <div className={styles.brandIcon}><Sparkles size={19} /></div>
          <div>
            <strong>AIS Studio</strong>
            <span>INTELLIGENT AUTOMATION WORKSPACE</span>
          </div>
        </div>
        <div className={styles.topbarStatus}>
          <span className={styles.statusDot} />
          <span>Local draft</span>
          <span className={styles.topbarDivider} />
          <span>CoreRPA v1</span>
        </div>
        <div className={styles.topbarActions}>
          <button type="button" className={styles.secondaryButton} onClick={() => saveWorkflow()} disabled={isBusy}>
            <Save size={15} /> Save
          </button>
          <button type="button" className={styles.primaryButton} onClick={runWorkflow} disabled={isBusy}>
            <Play size={15} fill="currentColor" /> Run workflow
          </button>
        </div>
      </header>

      <div className={styles.workspace}>
        <aside className={styles.sidebar}>
          <div className={styles.projectLabel}>WORKSPACE</div>
          <button className={`${styles.sideLink} ${styles.activeSideLink}`} type="button">
            <Workflow size={16} /> Workflow designer
          </button>
          <button className={styles.sideLink} type="button" onClick={() => setView("testing")}>
            <Activity size={16} /> Test & debugger
          </button>
          <button className={styles.sideLink} type="button" onClick={() => setView("runtime")}>
            <Monitor size={16} /> Runtime settings
          </button>
          <button className={styles.sideLink} type="button" onClick={() => setView("publish")}>
            <Upload size={16} /> Orchestrator
          </button>
          <div className={styles.sidebarRule} />
          <div className={styles.projectLabel}>RECENT RUNS</div>
          {executions.slice(0, 4).map((execution) => (
            <div className={styles.recentRun} key={execution.id}>
              <span className={styles.runIndicator} />
              <span className={styles.recentRunText}>
                <strong>{execution.status.toLowerCase().replaceAll("_", " ")}</strong>
                <small>{execution.id.slice(0, 12)}</small>
              </span>
            </div>
          ))}
          {executions.length === 0 && <p className={styles.sidebarEmpty}>Connect to load recent runs.</p>}
          <div className={styles.sidebarFooter}>
            <ShieldCheck size={15} />
            <span>Tenant-scoped workspace</span>
          </div>
        </aside>

        <section className={styles.mainArea}>
          <div className={styles.workflowBar}>
            <div className={styles.breadcrumbs}>
              <span>AIS Projects</span><span className={styles.breadcrumbSep}>/</span>
              <strong>{workflowName || "Untitled workflow"}</strong>
              <ChevronDown size={14} />
            </div>
            <div className={styles.workflowMeta}>
              <span className={styles.draftPill}>{selectedWorkflow?.status ?? "DRAFT"}</span>
              <span>Version {typeof selectedWorkflow?.version === "number" ? selectedWorkflow.version : 1}</span>
              <span className={styles.metaDivider} />
              <span>{steps.length} activities</span>
            </div>
          </div>

          <nav className={styles.viewTabs} aria-label="Studio sections">
            {runtimeViews.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  type="button"
                  key={item.id}
                  className={view === item.id ? styles.activeTab : ""}
                  onClick={() => setView(item.id)}
                >
                  <Icon size={15} /> {item.label}
                </button>
              );
            })}
            <div className={styles.viewTabsRight}>
              <span><span className={styles.statusDot} /> Autosaved locally</span>
            </div>
          </nav>

          {(error || notice) && (
            <div className={error ? styles.alertError : styles.alertNotice} role={error ? "alert" : "status"}>
              {error ? <CircleHelp size={16} /> : <Check size={16} />}
              <span>{error || notice}</span>
              <button type="button" aria-label="Dismiss message" onClick={() => { setError(""); setNotice(""); }}>
                <X size={15} />
              </button>
            </div>
          )}

          {view === "designer" && (
            <div className={styles.designer}>
              <aside className={styles.toolbox}>
                <div className={styles.panelTitle}>
                  <div><strong>Activities</strong><small>Click to add to your flow</small></div>
                  <button type="button" className={styles.iconButton} title="Activity toolbox"><Plus size={16} /></button>
                </div>
                <label className={styles.searchBox}>
                  <Code2 size={14} /><input aria-label="Search activities" placeholder="Search activities" />
                </label>
                <div className={styles.toolboxGroup}>
                  <span className={styles.groupLabel}>AIS CORE</span>
                  <button type="button" className={styles.activityItem} onClick={() => addStep("prompt")}>
                    <span className={`${styles.activityIcon} ${styles.aiIcon}`}><Sparkles size={16} /></span>
                    <span><strong>AI Prompt</strong><small>Generate model output</small></span><Plus size={14} />
                  </button>
                  <button type="button" className={styles.activityItem} onClick={() => addStep("set_variable")}>
                    <span className={`${styles.activityIcon} ${styles.variableIcon}`}><Braces size={16} /></span>
                    <span><strong>Set Variable</strong><small>Store a JSON value</small></span><Plus size={14} />
                  </button>
                </div>
                <div className={styles.toolboxGroup}>
                  <span className={styles.groupLabel}>RECORDER TOOLS</span>
                  <button type="button" className={styles.activityItem} onClick={() => setBrowserRecorderOpen(true)}>
                    <span className={`${styles.activityIcon} ${styles.browserIcon}`}><MousePointer2 size={16} /></span>
                    <span><strong>Browser recorder</strong><small>Extension required</small></span>
                  </button>
                  <button type="button" className={styles.activityItem} onClick={() => setView("runtime")}>
                    <span className={`${styles.activityIcon} ${styles.desktopIcon}`}><Monitor size={16} /></span>
                    <span><strong>Desktop recorder</strong><small>Windows agent required</small></span>
                  </button>
                  <button type="button" className={styles.activityItem} onClick={() => setSelectorOpen(true)}>
                    <span className={`${styles.activityIcon} ${styles.selectorIcon}`}><MousePointer2 size={16} /></span>
                    <span><strong>UI element selector</strong><small>Capture a locator</small></span>
                  </button>
                  <button type="button" className={styles.activityItem} onClick={() => setView("runtime")}>
                    <span className={`${styles.activityIcon} ${styles.captureIcon}`}><ScreenShare size={16} /></span>
                    <span><strong>Screen capture</strong><small>Capture a shared screen</small></span>
                  </button>
                </div>
                <div className={styles.toolboxNote}>
                  <ShieldCheck size={14} />
                  <p>Only contract v1 actions are added to the executable workflow.</p>
                </div>
              </aside>

              <section className={styles.canvasArea} aria-label="Workflow canvas">
                <div className={styles.canvasToolbar}>
                  <div>
                    <strong>Workflow</strong>
                    <span>{steps.length} activities · sequential flow</span>
                  </div>
                  <div className={styles.canvasTools}>
                    <button type="button" onClick={() => setSelectorOpen(true)} title="UI element selector"><MousePointer2 size={15} /></button>
                    <button type="button" onClick={() => setView("testing")} title="Test workflow"><Play size={15} /></button>
                  </div>
                </div>
                <div className={styles.canvas}>
                  <div className={styles.flowStart}><Play size={13} fill="currentColor" /> Start</div>
                  <div className={styles.flowLine} />
                  {steps.length === 0 && (
                    <div className={styles.emptyCanvas}>
                      <div><Workflow size={26} /></div>
                      <strong>Your workflow starts here</strong>
                      <span>Add an AI Prompt or Set Variable activity from the toolbox.</span>
                    </div>
                  )}
                  {steps.map((step, index) => {
                    const isSelected = selectedStepId === step.id;
                    const promptStep = step.type === "prompt";
                    return (
                      <div className={styles.flowNodeWrap} key={step.id}>
                        <button
                          type="button"
                          className={`${styles.flowNode} ${promptStep ? styles.promptNode : styles.variableNode} ${isSelected ? styles.selectedNode : ""}`}
                          onClick={() => setSelectedStepId(step.id)}
                          aria-pressed={isSelected}
                        >
                          <span className={styles.nodeStripe} />
                          <span className={styles.nodeIcon}>{promptStep ? <Sparkles size={15} /> : <Braces size={15} />}</span>
                          <span className={styles.nodeBody}>
                            <span className={styles.nodeType}>{formatStep(step)} <small>#{index + 1}</small></span>
                            <strong>{step.key || "Output key"}</strong>
                            <span className={styles.nodeSummary}>
                              {promptStep ? step.prompt || "Configure an AI prompt" : step.value || "Configure a JSON value"}
                            </span>
                            <span className={styles.nodeFoot}>AIS · Contract v1</span>
                          </span>
                          <span className={styles.nodeStatus}><Check size={12} /></span>
                        </button>
                        <div className={styles.nodeConnector} />
                      </div>
                    );
                  })}
                  <button type="button" className={styles.addNodeButton} onClick={() => addStep("prompt")}>
                    <Plus size={14} /> Add activity
                  </button>
                  <div className={styles.flowLine} />
                  <div className={styles.flowEnd}><Check size={13} /> End</div>
                </div>
                <div className={styles.canvasFooter}>
                  <span><Layers3 size={14} /> Workflow canvas</span>
                  <span>Drag activities from the toolbox to extend this flow</span>
                </div>
              </section>

              <aside className={styles.inspector}>
                <div className={styles.inspectorHeading}>
                  <div><strong>Properties</strong><small>{selectedStep ? "Selected activity" : "Workflow settings"}</small></div>
                  {selectedStep && (
                    <button type="button" className={styles.iconButton} title="Delete activity" onClick={() => deleteStep(selectedStep.id)}>
                      <Trash2 size={15} />
                    </button>
                  )}
                </div>
                {selectedStep ? (
                  <div className={styles.inspectorBody}>
                    <div className={styles.selectedActivity}>
                      <span className={selectedStep.type === "prompt" ? styles.aiIcon : styles.variableIcon}>
                        {selectedStep.type === "prompt" ? <Sparkles size={17} /> : <Braces size={17} />}
                      </span>
                      <span><strong>{formatStep(selectedStep)}</strong><small>AIS Runtime activity</small></span>
                    </div>
                    <label htmlFor="activity-output-key">Output key</label>
                    <input
                      id="activity-output-key"
                      value={selectedStep.key}
                      maxLength={64}
                      onChange={(event) => updateStep(selectedStep.id, { key: event.target.value })}
                      spellCheck={false}
                    />
                    {selectedStep.type === "prompt" ? (
                      <>
                        <label htmlFor="activity-prompt">Prompt template</label>
                        <textarea
                          id="activity-prompt"
                          rows={9}
                          value={selectedStep.prompt}
                          maxLength={8000}
                          onChange={(event) => updateStep(selectedStep.id, { prompt: event.target.value })}
                          spellCheck={false}
                        />
                        <p className={styles.fieldHint}>Reference input or earlier outputs with {"{{variable_name}}"}.</p>
                        <div className={styles.infoCard}><Bot size={15} /><span>Model calls run through the configured AIS runtime provider.</span></div>
                      </>
                    ) : (
                      <>
                        <label htmlFor="activity-value">JSON value</label>
                        <textarea
                          id="activity-value"
                          className={styles.jsonEditor}
                          rows={6}
                          value={selectedStep.value}
                          onChange={(event) => updateStep(selectedStep.id, { value: event.target.value })}
                          spellCheck={false}
                        />
                        <p className={styles.fieldHint}>Enter any valid JSON value: string, number, boolean, object or array.</p>
                      </>
                    )}
                    <div className={styles.orderControls}>
                      <button type="button" onClick={() => moveStep(selectedStep.id, -1)}><ArrowUp size={14} /> Move up</button>
                      <button type="button" onClick={() => moveStep(selectedStep.id, 1)}><ArrowDown size={14} /> Move down</button>
                    </div>
                  </div>
                ) : (
                  <div className={styles.inspectorBody}>
                    <div className={styles.workflowPropertiesIcon}><Workflow size={20} /></div>
                    <label htmlFor="workflow-name">Workflow name</label>
                    <input id="workflow-name" value={workflowName} maxLength={160} onChange={(event) => setWorkflowName(event.target.value)} />
                    <label className={styles.checkboxField}>
                      <input type="checkbox" checked={requiresApproval} onChange={(event) => setRequiresApproval(event.target.checked)} />
                      Require human approval before execution
                    </label>
                    <p className={styles.fieldHint}>Select an activity on the canvas to edit its properties.</p>
                  </div>
                )}
              </aside>
            </div>
          )}

          {view === "testing" && (
            <section className={styles.contentPanel}>
              <div className={styles.sectionHeading}>
                <div><span className={styles.eyebrow}>VALIDATE & INSPECT</span><h2>Workflow testing</h2><p>Validate the AIS contract and inspect a safe local dry-run. No external model call is made.</p></div>
                <button type="button" className={styles.primaryButton} onClick={validateWorkflow}><Play size={15} /> Run local dry-run</button>
              </div>
              <div className={styles.testGrid}>
                <div className={styles.formCard}>
                  <label htmlFor="test-input">Test input · JSON object</label>
                  <textarea id="test-input" className={styles.largeCode} value={inputText} onChange={(event) => setInputText(event.target.value)} rows={13} spellCheck={false} />
                  <div className={styles.testNote}><ShieldCheck size={15} /> Dry-run checks contract shape, prompt variables and JSON values. It does not execute AI or UI actions.</div>
                </div>
                <div className={styles.formCard}>
                  <div className={styles.cardHeading}><strong>Debugger output</strong><span>{debugLines.length} events</span></div>
                  <div className={styles.debugOutput} aria-live="polite">
                    {debugLines.map((line, index) => (
                      <div key={`${index}-${line}`}><span>{String(index + 1).padStart(2, "0")}</span><code>{line}</code></div>
                    ))}
                  </div>
                  <div className={styles.testNote}><Clock3 size={15} /> Use Run workflow to submit work to a licensed CoreRPA worker.</div>
                </div>
              </div>
            </section>
          )}

          {view === "runtime" && (
            <section className={styles.contentPanel}>
              <div className={styles.sectionHeading}>
                <div><span className={styles.eyebrow}>LOCAL & EXECUTION ENVIRONMENT</span><h2>Runtime configuration</h2><p>Set non-secret project defaults and check recorder capabilities. Credentials remain managed by your deployment.</p></div>
              </div>
              <div className={styles.runtimeGrid}>
                <div className={styles.formCard}>
                  <div className={styles.cardHeading}><strong><Settings2 size={16} /> AIS runtime defaults</strong><span>Saved in this browser</span></div>
                  <label htmlFor="runtime-model">Model provider profile</label>
                  <input id="runtime-model" value={runtimeModel} maxLength={100} onChange={(event) => setRuntimeModel(event.target.value)} />
                  <label htmlFor="runtime-endpoint">Provider endpoint (optional)</label>
                  <input id="runtime-endpoint" type="url" value={runtimeEndpoint} onChange={(event) => setRuntimeEndpoint(event.target.value)} placeholder="https://your-approved-provider.example" />
                  <label htmlFor="runtime-timeout">Request timeout · seconds</label>
                  <input id="runtime-timeout" type="number" min="1" max="3600" value={runtimeTimeout} onChange={(event) => setRuntimeTimeout(event.target.value)} />
                  <p className={styles.fieldHint}>These values are package metadata only. Configure provider secrets on the secured runtime agent.</p>
                </div>
                <div className={styles.formCard}>
                  <div className={styles.cardHeading}><strong><ScreenShare size={16} /> Capture tools</strong><span>{screenStream ? "Screen connected" : "No screen connected"}</span></div>
                  <p className={styles.runtimeDescription}>Capture a browser-visible screen share or a still frame for selector analysis.</p>
                  <div className={styles.captureActions}>
                    {!screenStream ? (
                      <button type="button" className={styles.secondaryButton} onClick={startScreenCapture}><ScreenShare size={15} /> Start screen capture</button>
                    ) : (
                      <>
                        <button type="button" className={styles.secondaryButton} onClick={captureFrame}><Download size={15} /> Capture frame</button>
                        <button type="button" className={styles.stopButton} onClick={stopScreenCapture}><Square size={13} fill="currentColor" /> Stop sharing</button>
                      </>
                    )}
                    <button type="button" className={styles.secondaryButton} onClick={() => setBrowserRecorderOpen(true)}><MousePointer2 size={15} /> Browser recorder</button>
                  </div>
                  {screenStream && <video ref={videoRef} className={styles.screenPreview} autoPlay muted playsInline />}
                  {screenImage && <Image className={styles.screenPreview} src={screenImage} alt="Captured screen frame" width={960} height={540} unoptimized />}
                  {!screenStream && !screenImage && (
                    <div className={styles.agentNotice}><Monitor size={18} /><span><strong>Desktop recorder</strong><small>Full desktop recording and UI automation require a connected Windows Agent.</small></span></div>
                  )}
                </div>
              </div>
            </section>
          )}

          {view === "publish" && (
            <section className={styles.contentPanel}>
              <div className={styles.sectionHeading}>
                <div><span className={styles.eyebrow}>GOVERNED DEPLOYMENT</span><h2>Publish to Orchestrator</h2><p>Save versioned workflow definitions and request work through your tenant&apos;s existing licensed runtime.</p></div>
                <button type="button" className={styles.primaryButton} onClick={() => saveWorkflow(true)} disabled={isBusy}><Upload size={15} /> Publish workflow</button>
              </div>
              <div className={styles.publishGrid}>
                <div className={styles.formCard}>
                  <div className={styles.cardHeading}><strong>Orchestrator connection</strong><span>{workflows.length ? `${workflows.length} AIS workflows` : "Not connected"}</span></div>
                  <label htmlFor="ais-token">Tenant-scoped access token</label>
                  <input id="ais-token" type="password" autoComplete="off" value={token} onChange={(event) => setToken(event.target.value)} placeholder="Paste an access token for this session" />
                  <p className={styles.fieldHint}>Token is kept in memory for this page session and sent only to the configured CoreRPA API.</p>
                  <div className={styles.connectionButtons}>
                    <button type="button" className={styles.secondaryButton} onClick={loadData} disabled={isBusy}><Activity size={15} /> {isBusy ? "Connecting..." : "Connect & sync"}</button>
                    <button type="button" className={styles.secondaryButton} onClick={downloadPackage}><Package size={15} /> Build package</button>
                  </div>
                  {workflows.length > 0 && (
                    <>
                      <label htmlFor="existing-workflow">Workflow to update or run</label>
                      <select id="existing-workflow" value={selectedWorkflowId} onChange={(event) => setSelectedWorkflowId(event.target.value)}>
                        <option value="">Select workflow</option>
                        {workflows.map((workflow) => <option key={workflow.id} value={workflow.id}>{workflow.name} · {workflow.status}</option>)}
                      </select>
                    </>
                  )}
                  <label className={styles.checkboxField}>
                    <input type="checkbox" checked={requiresApproval} onChange={(event) => setRequiresApproval(event.target.checked)} />
                    Require human approval before execution
                  </label>
                </div>
                <div className={styles.formCard}>
                  <div className={styles.cardHeading}><strong>Deployment status</strong><span><span className={styles.statusDot} /> {publishedWorkflows.length} published</span></div>
                  <div className={styles.deploymentMetric}>
                    <div><span>Workflow lifecycle</span><strong>{selectedWorkflow?.status ?? "LOCAL DRAFT"}</strong></div>
                    <div><span>Published workflows</span><strong>{publishedWorkflows.length}</strong></div>
                    <div><span>Active executions</span><strong>{activeExecutionCount}</strong></div>
                  </div>
                  <div className={styles.securityNote}><ShieldCheck size={18} /><span><strong>Governed execution</strong><small>Runs are subject to tenant roles, license entitlements, approval gates, audit events and an active runtime worker.</small></span></div>
                  <div className={styles.cardHeading}><strong>Recent executions</strong><button type="button" className={styles.textButton} onClick={loadData} disabled={isBusy}>Refresh</button></div>
                  {executions.length === 0 ? (
                    <p className={styles.fieldHint}>Connect to the orchestrator to view execution history.</p>
                  ) : (
                    <div className={styles.executionList}>
                      {executions.slice(0, 6).map((execution) => (
                        <div key={execution.id}><span className={styles.executionState}>{execution.status}</span><code>{execution.id.slice(0, 18)}</code>{typeof execution.error_message === "string" && execution.error_message && <small>{execution.error_message}</small>}</div>
                      ))}
                    </div>
                  )}
                  {draftWorkflows.length > 0 && <p className={styles.fieldHint}>{draftWorkflows.length} draft workflow(s) available for publishing.</p>}
                </div>
              </div>
              <div className={styles.packageStrip}>
                <FileJson2 size={18} /><div><strong>Package Builder</strong><span>Export the AIS contract and non-secret runtime defaults as a portable JSON package.</span></div>
                <button type="button" className={styles.secondaryButton} onClick={downloadPackage}><Download size={15} /> Export package</button>
              </div>
            </section>
          )}

          <section className={styles.debugPanel}>
            <div className={styles.debugPanelHeader}>
              <div><Activity size={15} /><strong>Debugger logs</strong><span>{debugLines.length} lines</span></div>
              <button type="button" onClick={() => setDebugLines([])} title="Clear logs"><Trash2 size={14} /></button>
            </div>
            <div className={styles.debugPanelBody}>
              {debugLines.length === 0 ? <span className={styles.debugPlaceholder}>No debugger events yet.</span> : debugLines.slice(-3).map((line, index) => (
                <div key={`${index}-${line}`}><span>●</span>{line}</div>
              ))}
            </div>
          </section>
        </section>
      </div>

      {selectorOpen && (
        <div className={styles.modalBackdrop} role="presentation" onMouseDown={(event) => {
          if (event.target === event.currentTarget) setSelectorOpen(false);
        }}>
          <section className={styles.modal} role="dialog" aria-modal="true" aria-labelledby="selector-title">
            <div className={styles.modalHeader}><div><span className={styles.activityIcon}><MousePointer2 size={16} /></span><div><h2 id="selector-title">UI element selector</h2><p>Store a locator for use by a connected recorder activity.</p></div></div><button type="button" onClick={() => setSelectorOpen(false)} aria-label="Close selector"><X size={18} /></button></div>
            <div className={styles.selectorNotice}><CircleHelp size={16} /> A web page cannot inspect another tab or desktop by itself. Use the approved browser extension or Windows Agent to capture live selectors.</div>
            <label htmlFor="selector-value">CSS selector or accessible name</label>
            <input id="selector-value" value={selectorValue} onChange={(event) => setSelectorValue(event.target.value)} placeholder='e.g. button[aria-label="Continue"]' />
            <div className={styles.modalActions}><button type="button" className={styles.secondaryButton} onClick={() => setSelectorOpen(false)}>Close</button><button type="button" className={styles.primaryButton} onClick={copySelector}><Code2 size={15} /> Copy locator</button></div>
          </section>
        </div>
      )}

      {browserRecorderOpen && (
        <div className={styles.modalBackdrop} role="presentation" onMouseDown={(event) => {
          if (event.target === event.currentTarget) setBrowserRecorderOpen(false);
        }}>
          <section className={styles.modal} role="dialog" aria-modal="true" aria-labelledby="recorder-title">
            <div className={styles.modalHeader}><div><span className={styles.activityIcon}><MousePointer2 size={16} /></span><div><h2 id="recorder-title">Browser recorder</h2><p>Record web actions into a workflow.</p></div></div><button type="button" onClick={() => setBrowserRecorderOpen(false)} aria-label="Close recorder information"><X size={18} /></button></div>
            <div className={styles.recorderFeature}><Monitor size={20} /><div><strong>Connect an approved browser extension</strong><p>Browser pages cannot observe or record interactions in other tabs without an installed extension. Screen capture is available in Runtime settings; live action recording requires the companion recorder.</p></div></div>
            <div className={styles.recorderFeature}><ShieldCheck size={20} /><div><strong>Desktop recording</strong><p>Windows UI automation and desktop recording are handled by a tenant-provisioned CoreRPA Windows Agent, not by this web page.</p></div></div>
            <div className={styles.modalActions}><button type="button" className={styles.secondaryButton} onClick={() => { setBrowserRecorderOpen(false); setView("runtime"); }}>Open runtime settings</button><button type="button" className={styles.primaryButton} onClick={() => setBrowserRecorderOpen(false)}>Got it</button></div>
          </section>
        </div>
      )}
    </main>
  );
}
