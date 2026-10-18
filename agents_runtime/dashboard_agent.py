import json
import os

IMPORT_FILE = r"C:\tekla-mcp\import_summary.json"

DASHBOARD_FILE = r"C:\tekla-mcp\dashboard.json"


def main():

    if not os.path.exists(
        IMPORT_FILE
    ):

        print()
        print(
            "ERROR: import_summary.json not found"
        )

        return

    with open(
        IMPORT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        summary = json.load(f)

    total = summary["total"]

    created = summary["created"]

    failed = summary["failed"]

    skipped = summary["skipped"]

    active_members = (
        total - skipped
    )

    recovery_rate = round(
        (
            created / active_members
        ) * 100,
        2
    )

    dashboard = {
        "total_members": total,
        "created": created,
        "failed": failed,
        "skipped": skipped,
        "recovery_rate": recovery_rate,
        "status": "SUCCESS"
    }

    with open(
        DASHBOARD_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            dashboard,
            f,
            indent=4
        )

    print()
    print("STEEL AI MIND DASHBOARD")
    print("=======================")

    print(
        f"Total Members : {total}"
    )

    print(
        f"Created       : {created}"
    )

    print(
        f"Failed        : {failed}"
    )

    print(
        f"Skipped       : {skipped}"
    )

    print(
        f"Recovery Rate : {recovery_rate}%"
    )

    print()
    print(
        f"Dashboard Saved : {DASHBOARD_FILE}"
    )


if __name__ == "__main__":

    main()