# ApexiveAI Enterprise Operations Platform (AEOP)

ApexiveAI-owned, modular, multi-tenant enterprise operations platform.

## Phase 1 foundation
- FastAPI backend
- PostgreSQL database
- SQLAlchemy 2.x
- Keycloak JWT/JWKS authentication
- Tenant-scoped API access
- Role-based authorization
- Audit event foundation
- Health and readiness endpoints

This is a clean standalone foundation. It does not use any client/customer brand names.

## Requirements
- Windows 11
- Python 3.11+
- PostgreSQL 15+ (or Docker Desktop)
- VS Code

## Setup (Windows CMD)
```cmd
cd ApexiveAI-Enterprise-Operations-Platform
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` before starting. Set the Keycloak issuer and audience to the values configured in your realm/client.

Start PostgreSQL:
```cmd
docker compose up -d db
```

Start API:
```cmd
uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload
```

Open:
- API docs: http://127.0.0.1:8010/docs
- Health: http://127.0.0.1:8010/health
- Readiness: http://127.0.0.1:8010/ready

## Important security notes
- Do not commit `.env`.
- Configure Keycloak to issue access tokens with the expected `iss` and `aud`.
- Add tenant and role claims using a Keycloak protocol mapper.
- Use HTTPS in deployed environments.
- This foundation deliberately does not create public registration or a default administrator.
- Database schema creation is intentionally handled by Alembic in the next implementation step; this first scaffold includes SQLAlchemy models and a development-only `create_all` option.

## Initial API
- `GET /health`
- `GET /ready`
- `GET /api/v1/me`
- `GET /api/v1/tenants/current`
- `GET /api/v1/audit/recent`

The API requires a valid Keycloak access token for `/api/v1/*`.

## Industry modules

The public services module provides tenant-scoped service case and emergency
incident workflows, plus models for engineering supervision, policing and
dispatch, citizen services, city operations, campuses, and elderly care.
The manufacturing module provides tenant-scoped production order and industrial
metric workflows, with models for factories, equipment, quality, maintenance,
supply chain, warehouses, energy, ERP integrations, and operational KPIs.

Both modules are registered through `app.modules.main` and included by the
FastAPI application. Their product catalogs and tenant-scoped overviews are
available at:

- `GET /api/v1/public-services/catalog`
- `GET /api/v1/public-services/overview`
- `GET /api/v1/manufacturing/catalog`
- `GET /api/v1/manufacturing/overview`

Core workflow endpoints include `POST`/`GET /api/v1/public-services/cases`,
`POST`/`GET /api/v1/public-services/incidents`,
`POST`/`GET /api/v1/manufacturing/facilities`,
`POST`/`GET /api/v1/manufacturing/equipment`,
`POST`/`GET /api/v1/manufacturing/data-sources`,
`POST`/`GET /api/v1/manufacturing/production-orders`, and
`POST`/`GET /api/v1/manufacturing/metrics`. External ERP, GIS, PLC, SCADA, and
IoT connectivity must be configured and implemented per deployment; these
modules provide integration and data contracts, not live third-party links.

## Professional Services modules

The Professional Services API is registered under `/api/v1/professional-services`
and requires the same authenticated tenant context as the other `/api/v1/*`
endpoints. Its four domains expose tenant-scoped create, list, detail, and
partial-update operations, plus an `/overview` count endpoint:

- `consultation`: projects, assessments, strategies, roadmaps, deliverables
- `operation`: projects, customer insights, campaigns, tasks, performance
- `integration`: projects, systems, connectors, APIs, data mappings, sync jobs
- `kubernetes`: clusters, nodes, namespaces, workloads, deployments, migrations,
  maintenance

Collection endpoints support `limit` and `offset`. Related record identifiers
are checked against the current tenant. Integration credentials and Kubernetes
credentials are represented by secret-manager references; the API does not
store credential values or connect to live third-party/Kubernetes systems.
These modules provide the tenant-scoped inventory and workflow records, not
execution agents for sync jobs, deployments, or migrations.

## AEOP product portfolio

The Products API exposes the 13-product AEOP catalog and tenant-scoped product
deployment records. All `/api/v1/products/*` routes require a valid access
token and use the token's tenant claim to scope deployment data.

- `GET /api/v1/products/catalog` — product families and capabilities
- `GET /api/v1/products/overview` — tenant deployment counts by product and status
- `POST` / `GET /api/v1/products/deployments` — create and list product deployments
- `GET /api/v1/products/deployments/{deployment_id}` — read a deployment
- `PATCH /api/v1/products/deployments/{deployment_id}` — update deployment name,
  environment, status, configuration or integration references

Deployment configuration and integration references are inventory metadata;
they do not store credentials or provision live third-party services. The
`product_deployments` table is registered with the SQLAlchemy metadata and is
created by the existing development-only `create_all` option.

## Apexive CoreRPA

CoreRPA is registered under `/api/v1/automation` and uses the caller's
verified tenant claim for every persisted resource. The backend includes
versioned workflows, a bounded declarative runtime, bot registration and
controls, queued executions, cron schedules, event triggers, independent
approvals, monitoring, exception history, templates, analytics, audit records,
tenant execution limits, encrypted credential metadata, and tenant-scoped
software licensing.

Configure `AEOP_AUTOMATION_CREDENTIAL_KEY` with a stable, high-entropy value of
at least 32 characters before using the credential vault. The API accepts
credential values only when creating them; read responses never expose the
encrypted value or plaintext. Rotate and back up this key through the
deployment's secret manager.

Start the queue/schedule worker separately from the API process:

```cmd
cd backend
.venv\Scripts\python.exe -m app.modules.automation.runtime.worker
```

The worker claims tenant-scoped queue items with database row locks, dispatches
due schedules, enforces tenant concurrency/daily limits, and records execution
results and audit events. Configure this as a supervised service in production.
The visual workflow runtime supports the bounded actions `set_variable`,
`condition`, `for_each`, `while`, `parallel`, `component`, and `log`; it does
not evaluate Python, shell commands, or arbitrary scripts.

Connector records and host allowlists are available for REST API, browser,
database, file, document, desktop, and email integrations. Their live execution
adapters are not enabled by these metadata endpoints; workflows reject external
system actions until an adapter is separately implemented, reviewed, and
approved. Registered targets require an exact host allowlist, and credential
references are tenant-scoped.

The key endpoints are:

- `GET /api/v1/automation/overview`
- `GET` / `POST /api/v1/automation/workflows`; `PATCH` a workflow to publish it
- `POST /api/v1/automation/workflows/{workflow_id}/executions`
- `GET /api/v1/automation/bots`; `POST` bot registration and `/control`
- `GET /api/v1/automation/executions`; `POST /executions/{id}/run`
- `GET /api/v1/automation/queues`; `POST /queues/{id}/retry`
- `GET` / `POST /api/v1/automation/schedules`, `/triggers`, `/integrations`,
  `/templates`, and `/credentials`
- `GET /api/v1/automation/approvals`; `POST /approvals/{id}/decision`
- `GET /api/v1/automation/monitoring`, `/exceptions`, `/analytics`,
  `/governance`, and `/audit`

### CoreRPA sales and license lifecycle

The CoreRPA licensing workspace is `/licenses`; its APIs are under
`/api/v1/core-rpa`. Tenant users can request process assessments, PoCs,
professional services, or software quotations. Only tokens with a `sales`,
`sales_admin`, `platform_admin`, `system_admin`, or `super_admin` role can
issue quotations or verify payments. Customer order, agreement, payment
reference, license, developer-seat, usage, and renewal records are tenant
scoped.

The software order lifecycle is quotation → order → agreement acceptance →
invoice/bank-transfer reference → sales verification → tenant-account license
activation. Payment references are not treated as proof of payment. The
customer does not receive a signed standalone license key; authorization is
attached to the verified AEOP tenant. Developer seats, bot registrations, and
monthly execution totals are checked against active entitlements. Sales can
prepare renewal quotations for licenses expiring within a selected window at
`POST /api/v1/core-rpa/renewals/prepare`; renewal prices are copied from the
last license order and flagged for review before sharing.

Main endpoints:

- `POST` / `GET /api/v1/core-rpa/opportunities`
- `PATCH /api/v1/core-rpa/opportunities/{id}/quotation` (sales role)
- `POST /api/v1/core-rpa/opportunities/{id}/orders`
- `POST /api/v1/core-rpa/orders/{id}/agreement` and `/payment`
- `POST /api/v1/core-rpa/orders/{id}/payment-decision` (sales role)
- `GET /api/v1/core-rpa/licenses`, `/usage`, and `/developers`
- `POST /api/v1/core-rpa/licenses/{id}/renewal`
- `POST` / `GET /api/v1/core-rpa/renewals/prepare` and `/renewals/due`
- `POST` / `DELETE /api/v1/core-rpa/developers`

Licensing tables are included in SQLAlchemy metadata and development
`create_all`. This repository has no production migration workflow; create and
apply migrations before deployment. Review and publish a legally approved
license agreement and invoice/bank-transfer instructions before accepting
production orders. Renewal quotation preparation is an authenticated sales
operation and must be scheduled operationally or run from the sales console.

Mutation roles are `admin`, `developer`, and `operator` according to the
operation. Viewers have read-only access. Approval requesters cannot approve
their own executions. Automation tables are registered with SQLAlchemy
metadata; development `create_all` creates them, while production deployments
must apply their database migration before enabling the module.
