import json
from collections import defaultdict

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"

with open(PAYLOAD, "r") as f:
    data = json.load(f)

node_map = defaultdict(list)

for m in data["members"]:

    node_map[
        m["START_NODE"]
    ].append(m)

    node_map[
        m["END_NODE"]
    ].append(m)

print()
print("BRACE NODE REPORT")
print("=" * 60)

for member in data["members"]:

    profile = member["PROFILE"]

    if not profile.startswith("L"):
        continue

    nodes = [
        member["START_NODE"],
        member["END_NODE"]
    ]

    print()
    print(
        f"BRACE {member['MEMBER_ID']}"
    )

    for node in nodes:

        connected = node_map[node]

        print(
            f"Node {node} : "
            f"{len(connected)} members"
        )

        for c in connected:

            print(
                f"   {c['MEMBER_ID']} | "
                f"{c['PROFILE']} | "
                f"{c['GROUP']}"
            )