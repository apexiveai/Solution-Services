import sys
from pathlib import Path

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
    print("=== COMPOSITE FOREIGN KEY AUDIT ===")

    for name in TABLE_NAMES:
        table = Base.metadata.tables[name]

        print(f"\nTABLE: {name}")

        unique_pairs = []

        for constraint in table.constraints:
            columns = [
                column.name for column in constraint.columns
            ]

            if len(columns) >= 2:
                print(
                    f"  CONSTRAINT: {type(constraint).__name__}"
                    f" | columns={columns}"
                )

            if (
                "tenant_id" in columns
                and "id" in columns
            ):
                unique_pairs.append(columns)

        print(
            "  TENANT + ID UNIQUE/PK:",
            unique_pairs if unique_pairs else "NOT FOUND"
        )

        for fk_constraint in table.foreign_key_constraints:
            local = [
                element.parent.name
                for element in fk_constraint.elements
            ]
            remote = [
                element.target_fullname
                for element in fk_constraint.elements
            ]

            print(
                f"  FK GROUP: {local} -> {remote}"
            )

    print("\n=== AUDIT COMPLETED ===")


if __name__ == "__main__":
    main()
