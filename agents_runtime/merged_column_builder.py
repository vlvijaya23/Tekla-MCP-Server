import json

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"
MERGES = r"C:\tekla-mcp\column_merge_candidates.json"

with open(PAYLOAD, "r") as f:
    payload = json.load(f)

with open(MERGES, "r") as f:
    chains = json.load(f)

member_lookup = {
    m["MEMBER_ID"]: m
    for m in payload["members"]
}

merged = []

for chain in chains:

    if chain["profile"] != "HE220A":
        continue

    if len(chain["members"]) > 4:
        continue

    first = member_lookup[
        chain["members"][0]
    ]

    last = member_lookup[
        chain["members"][-1]
    ]

    merged.append({
        "member_id":
            f"MERGED_{chain['members'][0]}",
        "profile":
            chain["profile"],
        "start_x":
            first["START_X"],
        "start_y":
            first["START_Y"],
        "start_z":
            first["START_Z"],
        "end_x":
            last["END_X"],
        "end_y":
            last["END_Y"],
        "end_z":
            last["END_Z"],
        "segments":
            chain["members"]
    })

print()
print("MERGED COLUMN BUILD")
print("=" * 60)

for item in merged:

    print()
    print(item)