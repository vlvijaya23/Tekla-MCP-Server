import csv

from tekla_mcp_server import (
    create_beam
)

path = r"C:\TeklaAssistant\tekla_payload_mapped.csv"

success_count = 0
fail_count = 0
processed = 0

MAX_IMPORT = 951  # change if needed


with open(
    path,
    "r",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        if processed >= MAX_IMPORT:
            break

        try:

            result = create_beam(
                profile=row["PROFILE"],
                start_x=float(row["START_X"]),
                start_y=float(row["START_Y"]),
                start_z=float(row["START_Z"]),
                end_x=float(row["END_X"]),
                end_y=float(row["END_Y"]),
                end_z=float(row["END_Z"]),
                name=row["NAME"]
            )

            processed += 1

            if result.get("status") == "success":

                success_count += 1

            else:

                fail_count += 1

                print()
                print("FAILED")
                print(row["NAME"])
                print(result)

        except Exception as ex:

            fail_count += 1

            print()
            print("EXCEPTION")
            print(row["NAME"])
            print(str(ex))

        if processed % 50 == 0:

            print()
            print(
                f"Processed : {processed}"
            )

            print(
                f"Success   : {success_count}"
            )

            print(
                f"Failed    : {fail_count}"
            )

print()
print("===================================")
print("IMPORT COMPLETE")
print("===================================")
print()

print(
    f"Processed : {processed}"
)

print(
    f"Success   : {success_count}"
)

print(
    f"Failed    : {fail_count}"
)