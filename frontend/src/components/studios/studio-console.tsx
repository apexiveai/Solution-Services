"use client";

import { AlertTriangle, Bot, Play, RefreshCw, ShieldCheck } from "lucide-react";
import { useCallback, useState } from "react";
import styles from "./studio-console.module.css";

type StudioRuntime = "AIS" | "CY";
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
  error_message: string | null;
};

function isRecord(value: unknown): value is ApiRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function recordsFrom(value: unknown): ApiRecord[] {
  if (Array.isArray(value)) {
    return value.filter(isRecord);
  }
  if (isRecord(value) && Array.isArray(value.items)) {
    return value.items.filter(isRecord);
  }
  return [];
}

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : "The request could not be completed.";
}

const apiBase =
  process.env.NEXT_PUBLIC_AEOP_API_URL?.replace(/\/+$/, "") ??
  "http://localhost:8010";

const initialDefinitions: Record<StudioRuntime, string> = {
  AIS: JSON.stringify(
    {
      runtime: "AIS",
      contract_version: 1,
      steps: [
        {
          type: "prompt",
          key: "summary",
          prompt: "Summarize the following text: {{text}}",
        },
      ],
    },
    null,
    2,
  ),
  CY: JSON.stringify(
    {
      runtime: "CY",
      contract_version: 1,
      rules: [
        {
          id: "failed-login",
          field: "event.type",
          equals: "failed_login",
          severity: "HIGH",
          title: "Repeated failed login",
          recommended_response: "Review the account and source activity.",
        },
      ],
    },
    null,
    2,
  ),
};

const initialInputs: Record<StudioRuntime, string> = {
  AIS: JSON.stringify({ text: "Add representative input before running." }, null, 2),
  CY: JSON.stringify({ events: [{ event: { type: "failed_login" } }] }, null, 2),
};

export default function StudioConsole({ runtime }: { runtime: StudioRuntime }) {
  const [token, setToken] = useState("");
  const [workflowName, setWorkflowName] = useState(
    runtime === "AIS" ? "New AIS workflow" : "New CY policy",
  );
  const [definitionText, setDefinitionText] = useState(initialDefinitions[runtime]);
  const [inputText, setInputText] = useState(initialInputs[runtime]);
  const [requiresApproval, setRequiresApproval] = useState(true);
  const [workflows, setWorkflows] = useState<WorkflowRecord[]>([]);
  const [executions, setExecutions] = useState<ExecutionRecord[]>([]);
  const [selectedWorkflowId, setSelectedWorkflowId] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const request = useCallback(
    async (path: string, accessToken: string, options: RequestInit = {}) => {
      const headers = new Headers(options.headers);
      headers.set("Authorization", `Bearer ${accessToken}`);
      if (options.body) {
        headers.set("Content-Type", "application/json");
      }

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
        const detail = isRecord(payload) && typeof payload.detail === "string"
          ? payload.detail
          : `CoreRPA API request failed (${response.status}).`;
        throw new Error(detail);
      }
      return payload;
    },
    [],
  );

  const loadData = useCallback(async () => {
    if (!token.trim()) {
      setError("Enter an access token to connect to the CoreRPA orchestrator.");
      return;
    }

    setIsLoading(true);
    setError("");
    setNotice("");
    try {
      const [workflowPayload, executionPayload] = await Promise.all([
        request("workflows?limit=100", token.trim()),
        request("executions?limit=100", token.trim()),
      ]);
      const matchingWorkflows = recordsFrom(workflowPayload)
        .filter((record) => {
          const definition = isRecord(record.definition) ? record.definition : {};
          return definition.runtime === runtime;
        })
        .filter(
          (record): record is WorkflowRecord =>
            typeof record.id === "string"
            && typeof record.name === "string"
            && typeof record.status === "string"
            && isRecord(record.definition),
        );
      const matchingExecutions = recordsFrom(executionPayload)
        .filter((record) => typeof record.workflow_id === "string")
        .filter((record) =>
          matchingWorkflows.some((workflow) => workflow.id === record.workflow_id),
        )
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
          : matchingWorkflows[0]?.id ?? "",
      );
      setNotice(`Loaded ${matchingWorkflows.length} ${runtime} workflows.`);
    } catch (requestError) {
      setError(errorMessage(requestError));
    } finally {
      setIsLoading(false);
    }
  }, [request, runtime, token]);

  async function createWorkflow() {
    if (!token.trim()) {
      setError("Enter an access token to save a workflow.");
      return;
    }
    setIsLoading(true);
    setError("");
    setNotice("");
    try {
      const definition: unknown = JSON.parse(definitionText);
      if (!isRecord(definition) || definition.runtime !== runtime) {
        throw new Error(`The workflow definition must target the ${runtime} runtime.`);
      }
      const created = await request("workflows", token.trim(), {
        method: "POST",
        body: JSON.stringify({
          name: workflowName,
          description: `${runtime} Studio workflow`,
          definition,
          requires_approval: requiresApproval,
        }),
      });
      if (!isRecord(created) || typeof created.id !== "string") {
        throw new Error("CoreRPA did not return the saved workflow.");
      }
      setSelectedWorkflowId(created.id);
      setNotice("Workflow saved. Runtime execution still requires an active CoreRPA license.");
      await loadData();
    } catch (requestError) {
      setError(errorMessage(requestError));
    } finally {
      setIsLoading(false);
    }
  }

  async function runWorkflow() {
    if (!selectedWorkflowId) {
      setError("Select or save a workflow before requesting execution.");
      return;
    }
    setIsLoading(true);
    setError("");
    setNotice("");
    try {
      const inputData: unknown = JSON.parse(inputText);
      if (!isRecord(inputData)) {
        throw new Error("Execution input must be a JSON object.");
      }
      await request(`workflows/${selectedWorkflowId}/executions`, token.trim(), {
        method: "POST",
        body: JSON.stringify({ input_data: inputData, priority: 5 }),
      });
      setNotice("Execution queued in the existing CoreRPA orchestrator.");
      await loadData();
    } catch (requestError) {
      setError(errorMessage(requestError));
    } finally {
      setIsLoading(false);
    }
  }

  async function publishWorkflow(workflowId: string) {
    setIsLoading(true);
    setError("");
    setNotice("");
    try {
      await request(`workflows/${workflowId}`, token.trim(), {
        method: "PATCH",
        body: JSON.stringify({ status: "PUBLISHED" }),
      });
      setNotice("Workflow published; execution remains subject to CoreRPA entitlements.");
      await loadData();
    } catch (requestError) {
      setError(errorMessage(requestError));
    } finally {
      setIsLoading(false);
    }
  }

  const Icon = runtime === "AIS" ? Bot : ShieldCheck;
  const title = runtime === "AIS" ? "AIS Studio" : "CY Studio";
  const subtitle =
    runtime === "AIS"
      ? "Build governed AI workflows and submit them to the licensed CoreRPA runtime."
      : "Define defensive alert policies and human-reviewed response recommendations.";

  return (
    <main className={styles.page}>
      <header className={styles.hero}>
        <div className={styles.heroIcon}><Icon size={28} /></div>
        <div>
          <span className={styles.eyebrow}>APEXIVE CORE RPA / {runtime} RUNTIME</span>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
      </header>

      <section className={styles.connection}>
        <label htmlFor={`${runtime}-token`}>Orchestrator access token</label>
        <div className={styles.connectionRow}>
          <input
            id={`${runtime}-token`}
            type="password"
            autoComplete="off"
            value={token}
            onChange={(event) => setToken(event.target.value)}
            placeholder="Paste a tenant-scoped access token"
          />
          <button type="button" onClick={loadData} disabled={isLoading}>
            <RefreshCw size={16} /> Connect
          </button>
        </div>
        <p>Token stays in this page session and is sent only to your configured CoreRPA API.</p>
      </section>

      {error && <div className={styles.error} role="alert"><AlertTriangle size={17} />{error}</div>}
      {notice && <div className={styles.notice} role="status">{notice}</div>}

      <div className={styles.columns}>
        <section className={styles.panel}>
          <div className={styles.panelHeading}>
            <div><span className={styles.eyebrow}>WORKFLOW DESIGN</span><h2>Define a workflow</h2></div>
          </div>
          <label htmlFor={`${runtime}-name`}>Workflow name</label>
          <input
            id={`${runtime}-name`}
            value={workflowName}
            onChange={(event) => setWorkflowName(event.target.value)}
            maxLength={160}
          />
          <label htmlFor={`${runtime}-definition`}>Version 1 workflow definition (JSON)</label>
          <textarea
            id={`${runtime}-definition`}
            className={styles.code}
            value={definitionText}
            onChange={(event) => setDefinitionText(event.target.value)}
            rows={17}
            spellCheck={false}
          />
          <label className={styles.checkbox}>
            <input
              type="checkbox"
              checked={requiresApproval}
              onChange={(event) => setRequiresApproval(event.target.checked)}
            />
            Require human approval before execution
          </label>
          <button type="button" className={styles.primary} onClick={createWorkflow} disabled={isLoading}>
            Save licensed workflow
          </button>
        </section>

        <section className={styles.panel}>
          <div className={styles.panelHeading}>
            <div><span className={styles.eyebrow}>ORCHESTRATION</span><h2>Queue an execution</h2></div>
          </div>
          <label htmlFor={`${runtime}-workflow`}>Published workflow</label>
          <select
            id={`${runtime}-workflow`}
            value={selectedWorkflowId}
            onChange={(event) => setSelectedWorkflowId(event.target.value)}
          >
            <option value="">Select a {runtime} workflow</option>
            {workflows.filter((workflow) => workflow.status === "PUBLISHED").map((workflow) => (
              <option key={workflow.id} value={workflow.id}>{workflow.name}</option>
            ))}
          </select>
          {workflows.some((workflow) => workflow.status === "DRAFT") && (
            <div className={styles.drafts}>
              <strong>Drafts</strong>
              {workflows.filter((workflow) => workflow.status === "DRAFT").map((workflow) => (
                <div className={styles.draft} key={workflow.id}>
                  <span>{workflow.name}</span>
                  <button
                    type="button"
                    onClick={() => publishWorkflow(workflow.id)}
                    disabled={isLoading}
                  >
                    Publish
                  </button>
                </div>
              ))}
            </div>
          )}
          <label htmlFor={`${runtime}-input`}>Execution input (JSON)</label>
          <textarea
            id={`${runtime}-input`}
            className={styles.code}
            value={inputText}
            onChange={(event) => setInputText(event.target.value)}
            rows={8}
            spellCheck={false}
          />
          <button type="button" className={styles.primary} onClick={runWorkflow} disabled={isLoading}>
            <Play size={16} /> Request execution
          </button>

          <div className={styles.listHeading}>
            <h3>Recent executions</h3>
            <button type="button" className={styles.refresh} onClick={loadData} disabled={isLoading}>
              <RefreshCw size={15} /> Refresh
            </button>
          </div>
          {executions.length === 0 ? (
            <p className={styles.empty}>No {runtime} executions found for this tenant.</p>
          ) : (
            <ul className={styles.executionList}>
              {executions.slice(0, 10).map((execution) => (
                <li key={execution.id}>
                  <span><strong>{execution.status}</strong><small>{execution.id}</small></span>
                  {typeof execution.error_message === "string" && execution.error_message && (
                    <small className={styles.executionError}>{execution.error_message}</small>
                  )}
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
      <p className={styles.governance}>
        Workflow creation and execution continue to use existing tenant roles, CoreRPA license
        entitlements, approval gates, audit events and quotation-to-activation lifecycle.
        A tenant must also provision a Windows Agent with the matching runtime capability.
      </p>
    </main>
  );
}
