import json
import math

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"

with open(PAYLOAD, "r") as f:
    data = json.load(f)

print()
print("BEAM ALIGNMENT CHECK")
print("=" * 50)

for m in data["members"]:

    if "_COLUMN" in m["GROUP"]:
        continue

    dx = abs(m["END_X"] - m["START_X"])
    dy = abs(m["END_Y"] - m["START_Y"])
    dz = abs(m["END_Z"] - m["START_Z"])

    if dz < 0.05:

        print(
            f"{m['MEMBER_ID']} | "
            f"{m['PROFILE']} | "
            f"Z={m['START_Z']:.3f}"
        )