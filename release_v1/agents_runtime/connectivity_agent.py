import json
from collections import defaultdict

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"

with open(PAYLOAD, "r") as f:
    data = json.load(f)

node_map = defaultdict(list)

for member in data["members"]:

    node_map[
        member["START_NODE"]
    ].append(member["MEMBER_ID"])

    node_map[
        member["END_NODE"]
    ].append(member["MEMBER_ID"])

print()
print("CONNECTIVITY REPORT")
print("=" * 40)

joint_count = 0

for node, members in node_map.items():

    if len(members) >= 3:

        joint_count += 1

        print(
            f"Node {node}: "
            f"{len(members)} members"
        )

print()
print(
    f"Detected Joints: {joint_count}"
)