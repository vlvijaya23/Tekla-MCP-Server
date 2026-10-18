"""
Steel AI Mind
Dashboard Agent
"""

import json
import os

SUMMARY_FILE = r"C:\tekla-mcp\import_summary.json"

if not os.path.exists(SUMMARY_FILE):

    print()
    print("STEEL AI MIND DASHBOARD")
    print("=======================")
    print("import_summary.json not found")

    raise SystemExit()

with open(
    SUMMARY_FILE,
    "r",
    encoding="utf-8"
) as f:

    summary = json.load(f)

total = summary.get("total", 0)
created = summary.get("created", 0)
failed = summary.get("failed", 0)
skipped = summary.get("skipped", 0)

attempted = created + failed

if attempted > 0:

    recovery = (
        created / attempted
    ) * 100

else:

    recovery = 0

dashboard = {
    "total": total,
    "created": created,
    "failed": failed,
    "skipped": skipped,
    "recovery_rate": round(
        recovery,
        2
    )
}

with open(
    r"C:\tekla-mcp\dashboard.json",
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

print(f"Total Members : {total}")
print(f"Created       : {created}")
print(f"Failed        : {failed}")
print(f"Skipped       : {skipped}")
print(
    f"Recovery Rate : {recovery:.2f}%"
)

print()
print(
    "Dashboard Saved : "
    r"C:\tekla-mcp\dashboard.json"
)