import json
from collections import defaultdict

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"

with open(PAYLOAD, "r") as f:
    data = json.load(f)

node_map = defaultdict(list)

for member in data["members"]:

    if "_COLUMN" not in member["GROUP"]:
        continue

    node_map[
        member["START_NODE"]
    ].append(member["MEMBER_ID"])

    node_map[
        member["END_NODE"]
    ].append(member["MEMBER_ID"])

print()
print("COLUMN CONTINUITY REPORT")
print("=" * 40)

for node, members in node_map.items():

    if len(members) > 1:

        print(
            f"Node {node} -> {members}"
        )