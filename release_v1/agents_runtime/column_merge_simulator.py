import json

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"
MERGES = r"C:\tekla-mcp\column_merge_candidates.json"

with open(PAYLOAD, "r") as f:
    payload = json.load(f)

with open(MERGES, "r") as f:
    merge_candidates = json.load(f)

members = payload["members"]

member_lookup = {
    m["MEMBER_ID"]: m
    for m in members
}

merged_members = []
merged_ids = set()

for chain in merge_candidates:

    if chain["profile"] != "HE220A":
        continue

    first = member_lookup[
        chain["members"][0]
    ]

    last = member_lookup[
        chain["members"][-1]
    ]

    merged = dict(first)

    merged["END_X"] = last["END_X"]
    merged["END_Y"] = last["END_Y"]
    merged["END_Z"] = last["END_Z"]

    merged["MEMBER_ID"] = (
        f"MERGED_{chain['members'][0]}"
    )

    merged["MERGED_FROM"] = (
        chain["members"]
    )

    merged_members.append(
        merged
    )

    merged_ids.update(
        chain["members"]
    )

for m in members:

    if m["MEMBER_ID"] not in merged_ids:

        merged_members.append(m)

print()
print("COLUMN MERGE SIMULATION")
print("=" * 60)

print(
    f"Original Members : {len(members)}"
)

print(
    f"Merged Members   : {len(merged_members)}"
)

print()

for m in merged_members:

    if "MERGED_FROM" in m:

        print(
            f"{m['MEMBER_ID']} <- "
            f"{m['MERGED_FROM']}"
        )