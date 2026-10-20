import json

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"

with open(PAYLOAD, "r") as f:
    data = json.load(f)

member_map = {
    m["MEMBER_ID"]: m
    for m in data["members"]
}

chains = [
    [1, 14, 20],
    [2, 193, 15, 21],
    [4, 17, 23],
    [5, 195, 18, 24],
    [16, 140, 22],
    [19, 99, 223, 25]
]

print()
print("MERGED COLUMN GEOMETRY")
print("=" * 60)

for chain in chains:

    first = member_map[chain[0]]
    last = member_map[chain[-1]]

    print()

    print(
        f"Members : {chain}"
    )

    print(
        f"Profile : {first['PROFILE']}"
    )

    print(
        f"Start Node : {first['START_NODE']}"
    )

    print(
        f"End Node   : {last['END_NODE']}"
    )

    print(
        f"Start XYZ  : "
        f"({first['START_X']:.3f}, "
        f"{first['START_Y']:.3f}, "
        f"{first['START_Z']:.3f})"
    )

    print(
        f"End XYZ    : "
        f"({last['END_X']:.3f}, "
        f"{last['END_Y']:.3f}, "
        f"{last['END_Z']:.3f})"
    )