import json

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"

with open(PAYLOAD, "r") as f:
    data = json.load(f)

check_ids = [1, 14, 20, 17, 23]

print()
print("GEOMETRY CHECK")
print("=" * 60)

for m in data["members"]:

    if m["MEMBER_ID"] not in check_ids:
        continue

    dx = abs(m["END_X"] - m["START_X"])
    dy = abs(m["END_Y"] - m["START_Y"])
    dz = abs(m["END_Z"] - m["START_Z"])

    if dy > dx and dy > dz:
        member_type = "VERTICAL_AXIS_Y"

    elif dx > dy and dx > dz:
        member_type = "HORIZONTAL_AXIS_X"

    elif dz > dx and dz > dy:
        member_type = "VERTICAL_AXIS_Z"

    else:
        member_type = "DIAGONAL"

    print(
        f"ID={m['MEMBER_ID']} | "
        f"PROFILE={m['PROFILE']} | "
        f"dx={dx:.3f} dy={dy:.3f} dz={dz:.3f} | "
        f"{member_type}"
    )