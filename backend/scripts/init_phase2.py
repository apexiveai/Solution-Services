from app.database import Base, engine
from app import phase2

phase2_tables = [
    phase2.Tenant.__table__,
    phase2.Product.__table__,
    phase2.TenantLicense.__table__,
    phase2.Subscription.__table__,
    phase2.PlatformUser.__table__,
    phase2.AuditEvent.__table__,
]

Base.metadata.create_all(
    bind=engine,
    tables=phase2_tables,
)

print("AEOP Phase 2 database tables are ready.")
