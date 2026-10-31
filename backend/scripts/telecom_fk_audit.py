
import sys
from pathlib import Path

# Add backend root to Python import path
BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app import models  # noqa: E402
from app.modules.telecom import models as telecom_models  # noqa: E402
from app.database import Base  # noqa: E402


TABLE_NAMES = [
    "telecom_modules",
    "telecom_sites",
    "telecom_devices",
    "telecom_interfaces",
    "telecom_connections",
    "telecom_topology_links",
    "telecom_monitoring_sources",
    "telecom_metric_samples",
    "telecom_alarms",
    "telecom_incidents",
    "telecom_tenant_settings",
]


def main():
    print("=== TELECOM FOREIGN KEY AUDIT ===")

    missing = [
        name for name in TABLE_NAMES
        if name not in Base.metadata.tables
    ]

    if missing:
        print("MISSING TABLES:", missing)
        raise SystemExit(1)

    for table_name in TABLE_NAMES:
        table = Base.metadata.tables[table_name]

        print(f"\nTABLE: {table_name}")
        print(f"  tenant_id column: {'tenant_id' in table.c}")

        if "tenant_id" in table.c:
            tenant_fks = [
                fk.target_fullname
                for fk in table.c.tenant_id.foreign_keys
            ]
            print(f"  tenant_id references: {tenant_fks}")

        for column in table.columns:
            for fk in column.foreign_keys:
                print(
                    f"  FK: {column.name} -> {fk.target_fullname}"
                    f" | ondelete={fk.ondelete}"
                )

    print("\n=== TENANT CONSTRAINT SUMMARY ===")

    for table_name in TABLE_NAMES:
        table = Base.metadata.tables[table_name]

        if "tenant_id" not in table.c:
            print(f"{table_name}: NO DIRECT tenant_id")
            continue

        valid = any(
            fk.target_fullname == "tenants.id"
            for fk in table.c.tenant_id.foreign_keys
        )

        print(
            f"{table_name}: "
            f"{'PASS' if valid else 'CHECK REQUIRED'}"
        )

    print("\nAUDIT COMPLETED")


if __name__ == "__main__":
    main()
