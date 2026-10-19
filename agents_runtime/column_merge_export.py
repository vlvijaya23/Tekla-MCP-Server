import json

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"
OUTPUT = r"C:\tekla-mcp\column_merge_candidates.json"

with open(PAYLOAD, "r") as f:
    data = json.load(f)

columns = [
    m for m in data["members"]
    if "_COLUMN" in m["GROUP"]
]

chains = []
used = set()

for start_member in columns:

    if start_member["MEMBER_ID"] in used:
        continue

    chain = [start_member]
    current = start_member

    while True:

        next_member = None

        for candidate in columns:

            if candidate["MEMBER_ID"] == current["MEMBER_ID"]:
                continue

            if candidate["PROFILE"] != current["PROFILE"]:
                continue

            if candidate["START_NODE"] == current["END_NODE"]:

                next_member = candidate
                break

        if next_member is None:
            break

        chain.append(next_member)
        current = next_member

    if len(chain) > 1:

        for member in chain:
            used.add(member["MEMBER_ID"])

        chains.append(chain)

report = []

for chain in chains:

    report.append({
        "profile": chain[0]["PROFILE"],
        "members": [m["MEMBER_ID"] for m in chain],
        "start_node": chain[0]["START_NODE"],
        "end_node": chain[-1]["END_NODE"],
        "segment_count": len(chain)
    })

with open(OUTPUT, "w") as f:
    json.dump(
        report,
        f,
        indent=4
    )

print()
print("COLUMN MERGE FILE CREATED")
print(OUTPUT)
print()
print(f"Candidates: {len(report)}")