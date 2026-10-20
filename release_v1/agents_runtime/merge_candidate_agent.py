import json

PAYLOAD = r"C:\TeklaAssistant\staad_payload.json"

with open(PAYLOAD, "r") as f:
    data = json.load(f)

columns = [
    m for m in data["members"]
    if "_COLUMN" in m["GROUP"]
]

chains = []
used = set()

for start_member in columns:

    if start_member["MEMBER_ID"] in used:
        continue

    chain = [start_member]
    current = start_member

    while True:

        next_member = None

        for candidate in columns:

            if candidate["MEMBER_ID"] == current["MEMBER_ID"]:
                continue

            if candidate["PROFILE"] != current["PROFILE"]:
                continue

            if candidate["START_NODE"] == current["END_NODE"]:

                next_member = candidate
                break

        if next_member is None:
            break

        chain.append(next_member)
        current = next_member

    if len(chain) > 1:

        for member in chain:
            used.add(member["MEMBER_ID"])

        chains.append(chain)

print()
print("CONTINUOUS COLUMN CHAINS")
print("=" * 60)

for idx, chain in enumerate(chains, start=1):

    profile = chain[0]["PROFILE"]

    member_ids = [
        str(m["MEMBER_ID"])
        for m in chain
    ]

    start_node = chain[0]["START_NODE"]
    end_node = chain[-1]["END_NODE"]

    print()
    print(f"CHAIN {idx}")
    print(f"Profile     : {profile}")
    print(
        f"Members     : "
        f"{' -> '.join(member_ids)}"
    )
    print(
        f"Node Path   : "
        f"{start_node} -> {end_node}"
    )
    print(
        f"Segment Qty : "
        f"{len(chain)}"
    )
