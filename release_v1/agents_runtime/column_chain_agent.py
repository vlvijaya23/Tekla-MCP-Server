import json

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"

with open(PAYLOAD, "r") as f:
    data = json.load(f)

#
# Collect columns
#

columns = []

for m in data["members"]:

    if "_COLUMN" in m["GROUP"]:

        columns.append(m)

#
# Build node connectivity map
#

node_usage = {}

for m in data["members"]:

    start_node = m["START_NODE"]
    end_node = m["END_NODE"]

    node_usage.setdefault(
        start_node,
        []
    ).append(
        m["MEMBER_ID"]
    )

    node_usage.setdefault(
        end_node,
        []
    ).append(
        m["MEMBER_ID"]
    )

#
# Report
#

print()
print("COLUMN NODE CONNECTIVITY")
print("=" * 80)

for c in columns:

    start_node = c["START_NODE"]
    end_node = c["END_NODE"]

    start_refs = len(
        node_usage[start_node]
    )

    end_refs = len(
        node_usage[end_node]
    )

    merge_allowed = (
        start_refs <= 2
        and
        end_refs <= 2
    )

    print(
        f"ID {c['MEMBER_ID']:>4} | "
        f"{c['PROFILE']:<25} | "
        f"{start_node}({start_refs}) -> "
        f"{end_node}({end_refs}) | "
        f"MERGE={'YES' if merge_allowed else 'NO'}"
    )

#
# High connectivity nodes
#

print()
print("HIGH CONNECTIVITY NODES")
print("=" * 80)

for node_id in sorted(node_usage):

    refs = node_usage[node_id]

    if len(refs) > 2:

        print(
            f"NODE {node_id:>4} | "
            f"CONNECTED MEMBERS: "
            f"{refs}"
        )