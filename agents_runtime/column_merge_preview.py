import json

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"
MERGES = r"C:\tekla-mcp\column_merge_candidates.json"

with open(PAYLOAD, "r") as f:
    data = json.load(f)

with open(MERGES, "r") as f:
    chains = json.load(f)

member_lookup = {
    m["MEMBER_ID"]: m
    for m in data["members"]
}

print()
print("MERGED COLUMN PREVIEW")
print("=" * 60)

for chain in chains:

    first = member_lookup[
        chain["members"][0]
    ]

    last = member_lookup[
        chain["members"][-1]
    ]

    print()
    print(
        f"Members : {chain['members']}"
    )

    print(
        f"Profile : {chain['profile']}"
    )

    print(
        f"Start   : "
        f"({first['START_X']:.3f}, "
        f"{first['START_Y']:.3f}, "
        f"{first['START_Z']:.3f})"
    )

    print(
        f"End     : "
        f"({last['END_X']:.3f}, "
        f"{last['END_Y']:.3f}, "
        f"{last['END_Z']:.3f})"
    )

    print(
        f"Segments: "
        f"{chain['segment_count']}"
    )