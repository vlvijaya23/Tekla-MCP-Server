import json
import base64

machine_id = input(
    "Machine ID: "
)

license_data = {
    "company": "SLB",
    "expiry": "2027-12-31",
    "enabled": True,
    "machine_ids": [
        machine_id
    ]
}

encoded = base64.b64encode(
    json.dumps(
        license_data
    ).encode()
).decode()

with open(
    "license.key",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        encoded
    )

print(
    "license.key created"
)