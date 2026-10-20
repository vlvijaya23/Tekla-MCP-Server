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
print("COLUMN VALIDATION REPORT")
print("=" * 60)

for chain in chains:

    valid = True

    profile = member_map[
        chain[0]
    ]["PROFILE"]

    xs = []
    ys = []

    for member_id in chain:

        m = member_map[member_id]

        if m["PROFILE"] != profile:

            valid = False

        xs.extend(
            [
                round(m["START_X"], 3),
                round(m["END_X"], 3)
            ]
        )

        ys.extend(
            [
                round(m["START_Y"], 3),
                round(m["END_Y"], 3)
            ]
        )

    x_span = max(xs) - min(xs)
    y_span = max(ys) - min(ys)

    if x_span > 0.01:
        valid = False

    status = "VALID ✅" if valid else "REVIEW ⚠️"

    print()
    print(
        f"Chain: {chain}"
    )

    print(
        f"Profile: {profile}"
    )

    print(
        f"X Span: {x_span:.3f}"
    )

    print(
        f"Y Span: {y_span:.3f}"
    )

    print(
        f"Status: {status}"
    )