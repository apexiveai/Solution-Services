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
