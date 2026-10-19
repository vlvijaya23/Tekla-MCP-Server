import json

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"

with open(PAYLOAD, "r") as f:
    data = json.load(f)

columns = []

for m in data["members"]:

    if "_COLUMN" in m["GROUP"]:

        columns.append(m)

print()
print("COLUMN MEMBERS")
print("=" * 40)

for c in columns:

    print(
        f"ID {c['MEMBER_ID']} : "
        f"{c['PROFILE']} | "
        f"{c['START_NODE']} -> "
        f"{c['END_NODE']}"
    )