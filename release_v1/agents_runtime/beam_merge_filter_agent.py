import json

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"

with open(PAYLOAD, "r") as f:
    data = json.load(f)

print()
print("SAFE BEAM MERGE CANDIDATES")
print("=" * 60)

for m in data["members"]:

    if "_COLUMN" in m["GROUP"]:
        continue

    dz = abs(
        m["END_Z"] - m["START_Z"]
    )

    if dz > 0.01:
        continue

    print(
        f"{m['MEMBER_ID']} | "
        f"{m['PROFILE']} | "
        f"Z={m['START_Z']:.3f}"
    )