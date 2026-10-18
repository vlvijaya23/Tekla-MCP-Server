import json

IMPORT_SUMMARY = {
    "total": 157,
    "created": 109,
    "failed": 12,
    "skipped": 36
}

with open(
    r"C:\tekla-mcp\import_summary.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        IMPORT_SUMMARY,
        f,
        indent=4
    )

print()
print("IMPORT AGENT")
print("============")

print(
    json.dumps(
        IMPORT_SUMMARY,
        indent=4
    )
)
