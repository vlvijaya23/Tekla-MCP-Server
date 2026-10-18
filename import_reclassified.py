import csv
import math

from tekla_mcp_server import create_beam

path = r"C:\TeklaAssistant\tekla_payload_reclassified.csv"

MAX_IMPORT = 999999
SCALE = 1000.0
MAX_MEMBER_LENGTH = 12000.0

SKIP_PROFILES = {
    "SPECIAL",
    "EPBREBA",
    "EPBREBO",
    "EPCREBO",
    "EPBLTC",
    "ECCPF",
    "ECCCF",
    "PEYE",
    "ECCSTRI",
    "EPBLRTE",
    "T350*175",
    "L100*100*10",
    "L125*125*10",
    "C250X80"
}

success_count = 0
fail_count = 0
processed = 0
skipped_profiles = 0


def distance(x1, y1, z1, x2, y2, z2):

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2 +
        (z2 - z1) ** 2
    )


with open(path, "r", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        if processed >= MAX_IMPORT:
            break

        profile = row["PROFILE"]
        phase = row["PHASE"]

        if profile in SKIP_PROFILES:

            skipped_profiles += 1
            continue

        sx = float(row["START_X"]) * SCALE
        sy = float(row["START_Y"]) * SCALE
        sz = float(row["START_Z"]) * SCALE

        ex = float(row["END_X"]) * SCALE
        ey = float(row["END_Y"]) * SCALE
        ez = float(row["END_Z"]) * SCALE

        if sx == ex and sy == ey and sz == ez:
            continue

        member_length = distance(
            sx, sy, sz,
            ex, ey, ez
        )

        segments = max(
            1,
            math.ceil(
                member_length /
                MAX_MEMBER_LENGTH
            )
        )

        for segment in range(segments):

            t1 = segment / segments
            t2 = (segment + 1) / segments

            ssx = sx + (ex - sx) * t1
            ssy = sy + (ey - sy) * t1
            ssz = sz + (ez - sz) * t1

            eex = sx + (ex - sx) * t2
            eey = sy + (ey - sy) * t2
            eez = sz + (ez - sz) * t2

            result = create_beam(
                profile=profile,
                start_x=ssx,
                start_y=ssy,
                start_z=ssz,
                end_x=eex,
                end_y=eey,
                end_z=eez,
                name=f"{row['NAME']}_S{segment+1}",
                phase=phase
            )

            if result.get("status") == "success":

                success_count += 1

            else:

                fail_count += 1

        processed += 1

print()
print("=" * 50)
print("RECLASSIFIED IMPORT V2 COMPLETE")
print("=" * 50)

print(f"Processed        : {processed}")
print(f"Success          : {success_count}")
print(f"Failed           : {fail_count}")
print(f"Skipped Profiles : {skipped_profiles}")