"""
Tekla MCP Server
"""

import os
import sys
import pythonnet
import json
import math

sys.path.append(
    r"C:\tekla-mcp\agents_runtime"
)

from member_ai import process_member

from mcp.server.fastmcp import FastMCP

# ----------------------------------------------------
# MCP SERVER
# ----------------------------------------------------

mcp = FastMCP("tekla")

# ----------------------------------------------------
# TEKLA PATH
# ----------------------------------------------------

TEKLA_BIN = r"C:\TeklaStructures\2025.0\bin"

if not os.path.exists(TEKLA_BIN):
    raise Exception(
        f"Tekla installation not found: {TEKLA_BIN}"
    )

sys.path.append(TEKLA_BIN)

# ----------------------------------------------------
# LOAD PYTHONNET
# ----------------------------------------------------

pythonnet.load("netfx")

import clr

# ----------------------------------------------------
# LOAD TEKLA DLLS
# ----------------------------------------------------

DLLS = [
    "Tekla.Structures.dll",
    "Tekla.Structures.Model.dll",
    "Tekla.Structures.Drawing.dll"
]

for dll in DLLS:

    full_path = os.path.join(
        TEKLA_BIN,
        dll
    )

    if not os.path.exists(full_path):
        raise FileNotFoundError(
            f"Missing DLL: {full_path}"
        )

    print(f"Loading {dll}")

    clr.AddReference(full_path)

# ----------------------------------------------------
# EXTRA REFERENCES
# ----------------------------------------------------

clr.AddReference("Tekla.Structures")

# ----------------------------------------------------
# IMPORTS
# ----------------------------------------------------

from Tekla.Structures.Model import (
    Model,
    ModelObject,
    Beam,
    Position
)

from Tekla.Structures.Geometry3d import (
    Point
)

from Tekla.Structures.Model.UI import (
    ModelObjectSelector
)

print("Tekla assemblies loaded successfully")

# ----------------------------------------------------
# HELPERS
# ----------------------------------------------------

def get_model():

    model = Model()

    if not model.GetConnectionStatus():

        raise Exception(
            "Not connected to Tekla model"
        )

    return model

# ----------------------------------------------------
# PROFILE MAPPING
# ----------------------------------------------------

from core.profile_mapper import (
    map_profile,
    get_all_mappings,
    profile_exists,
    add_profile_mapping
)

def build_merged_members(
    members
):

    merge_file = (
        r"C:\tekla-mcp\column_merge_candidates.json"
    )

    with open(
        merge_file,
        "r",
        encoding="utf-8"
    ) as f:

        chains = json.load(f)

    member_lookup = {
        m["MEMBER_ID"]: m
        for m in members
    }

    merged_members = []
    merged_ids = set()

    for chain in chains:

        if chain["profile"] != "HE220A":
            continue

        first = member_lookup[
            chain["members"][0]
        ]

        last = member_lookup[
            chain["members"][-1]
        ]

        merged = dict(first)

        merged["END_X"] = last["END_X"]
        merged["END_Y"] = last["END_Y"]
        merged["END_Z"] = last["END_Z"]

        merged["MEMBER_ID"] = (
            f"MERGED_{chain['members'][0]}"
        )

        merged_members.append(
            merged
        )

        merged_ids.update(
            chain["members"]
        )

    for m in members:

        if m["MEMBER_ID"] not in merged_ids:

            merged_members.append(m)

    return merged_members

def split_long_member(
    member,
    max_length=12.0
):

    dx = (
        float(member["END_X"])
        - float(member["START_X"])
    )

    dy = (
        float(member["END_Y"])
        - float(member["START_Y"])
    )

    dz = (
        float(member["END_Z"])
        - float(member["START_Z"])
    )

    length = (
        dx ** 2 +
        dy ** 2 +
        dz ** 2
    ) ** 0.5

    if length <= max_length:

        return [member]

    count = math.ceil(
        length / max_length
    )

    segments = []

    for i in range(count):

        start_ratio = (
            i * max_length
        ) / length

        end_ratio = min(
            (
                (i + 1)
                * max_length
            ) / length,
            1.0
        )

        segment = dict(member)

        segment["START_X"] = (
            float(member["START_X"])
            + dx * start_ratio
        )

        segment["START_Y"] = (
            float(member["START_Y"])
            + dy * start_ratio
        )

        segment["START_Z"] = (
            float(member["START_Z"])
            + dz * start_ratio
        )

        segment["END_X"] = (
            float(member["START_X"])
            + dx * end_ratio
        )

        segment["END_Y"] = (
            float(member["START_Y"])
            + dy * end_ratio
        )

        segment["END_Z"] = (
            float(member["START_Z"])
            + dz * end_ratio
        )

        segment["MEMBER_ID"] = (
            f"{member['MEMBER_ID']}_S{i+1}"
        )

        segments.append(
            segment
        )

    return segments


def apply_length_limit(
    members
):

    final_members = []

    for member in members:

        final_members.extend(
            split_long_member(
                member,
                12.0
            )
        )

    return final_members

# ----------------------------------------------------
# MCP TOOLS
# ----------------------------------------------------

@mcp.tool()
def get_model_info():

    model = get_model()

    info = model.GetInfo()

    return {
        "model_name": info.ModelName,
        "model_path": info.ModelPath
    }


@mcp.tool()
def count_beams():

    model = get_model()

    selector = model.GetModelObjectSelector()

    beams = selector.GetAllObjectsWithType(
        ModelObject.ModelObjectEnum.BEAM
    )

    count = 0

    while beams.MoveNext():
        count += 1

    return count


@mcp.tool()
def list_beam_profiles_unique(limit: int = 200):

    model = get_model()

    selector = model.GetModelObjectSelector()

    beams = selector.GetAllObjectsWithType(
        ModelObject.ModelObjectEnum.BEAM
    )

    profiles = set()

    while beams.MoveNext():

        beam = beams.Current

        try:

            profiles.add(
                beam.Profile.ProfileString
            )

        except Exception:
            pass

        if len(profiles) >= limit:
            break

    return sorted(list(profiles))


@mcp.tool()
def selected_count():

    selector = ModelObjectSelector()

    selected = selector.GetSelectedObjects()

    count = 0

    while selected.MoveNext():
        count += 1

    return count


@mcp.tool()
def selected_profiles():

    selector = ModelObjectSelector()

    selected = selector.GetSelectedObjects()

    profiles = []

    while selected.MoveNext():

        obj = selected.Current

        try:

            profile = obj.Profile.ProfileString

            if profile not in profiles:
                profiles.append(profile)

        except Exception:
            pass

    return profiles


@mcp.tool()
def selected_objects():

    selector = ModelObjectSelector()

    selected = selector.GetSelectedObjects()

    result = []

    while selected.MoveNext():

        obj = selected.Current

        try:

            result.append(
                {
                    "id": obj.Identifier.ID,
                    "profile": obj.Profile.ProfileString
                }
            )

        except Exception:
            pass

    return result


@mcp.tool()
def create_beam(
    profile: str,
    start_x: float,
    start_y: float,
    start_z: float,
    end_x: float,
    end_y: float,
    end_z: float,
    name: str = "SACS_BEAM",
    phase: str = "UNCLASSIFIED"
):

    try:

        model = get_model()

        beam = Beam()

        beam.StartPoint = Point(
            start_x * 1000.0,
            start_z * 1000.0,
            start_y * 1000.0
        )

        beam.EndPoint = Point(
            end_x * 1000.0,
            end_z * 1000.0,
            end_y * 1000.0
        )

        beam.Profile.ProfileString = profile
        member_ai = process_member(
            member_id=0,
            profile=profile,
            start_x=start_x,
            start_y=start_y,
            start_z=start_z,
            end_x=end_x,
            end_y=end_y,
            end_z=end_z
        )
        
        beam.Material.MaterialString = (
            member_ai["classification"]["material"]
        )

        beam.Class = (
            member_ai["classification"]["class"]
        )

        phase = (
            member_ai["classification"]["phase"]
        )

        member_type = (
            member_ai["classification"]["member_type"]
        )

        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)
        dz = abs(end_z - start_z)

        horizontal = max(dx, dy)

        #
        # Naming
        #

        if member_type == "COLUMN":

            beam.Name = "COLUMN"

        else:

            beam.Name = "BEAM"

        #
        # Position
        #

        beam.Position.Plane = (
            Position.PlaneEnum.MIDDLE
        )

        if member_type == "COLUMN":

            beam.Position.Rotation = (
                Position.RotationEnum.FRONT
            )

            beam.Position.Depth = (
                Position.DepthEnum.MIDDLE
            )

        else:

            beam.Position.Rotation = (
                Position.RotationEnum.TOP
            )

            beam.Position.Depth = (
                Position.DepthEnum.BEHIND
            )

        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)
        dz = abs(end_z - start_z)

        horizontal = max(dx, dy)

        length = (
            (end_x - start_x) ** 2 +
            (end_y - start_y) ** 2 +
            (end_z - start_z) ** 2
        ) ** 0.5

        if length < 0.25:

            return {
                "status": "short_member",
                "length": length,
                "profile": profile,
                "name": beam.Name
            }

        success = beam.Insert()

        if success:

            model.CommitChanges()

            print(
                f"SUCCESS | {name} | "
                f"({start_x:.3f}, {start_y:.3f}, {start_z:.3f}) -> "
                f"({end_x:.3f}, {end_y:.3f}, {end_z:.3f})"
            )

            return {
                "status": "success",
                "name": beam.Name,
                "profile": profile,
                "phase": phase,
                "class": beam.Class
            }

        return {
            "status": "insert_failed",
            "name": beam.Name,
            "profile": profile,
            "length": length,
            "start": [
                start_x,
                start_y,
                start_z
            ],
            "end": [
                end_x,
                end_y,
                end_z
            ]
        }

    except Exception as ex:

        return {
            "status": "exception",
            "error": str(ex),
            "name": name,
            "profile": profile
        }

@mcp.tool()
def import_staad_json(
    json_file: str = r"C:\TeklaAssistant\data\staad_payload.json",
    limit: int = 10
):

    try:

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as f:

            payload = json.load(f)

        members = payload.get(
            "members",
            []
        )

        members = build_merged_members(
            members
        )

        members = apply_length_limit(
            members
        )

        if limit > 0:

            members = members[:limit]

        created = 0
        failed = 0
        skipped = 0
        errors = []

        for member in members:

            try:

                profile = map_profile(
                    member["PROFILE"]
                )

                result = create_beam(
                    profile=profile,
                    start_x=float(member["START_X"]),
                    start_y=float(member["START_Y"]),
                    start_z=float(member["START_Z"]),
                    end_x=float(member["END_X"]),
                    end_y=float(member["END_Y"]),
                    end_z=float(member["END_Z"]),
                    name=f"STAAD_{member['MEMBER_ID']}",
                    phase=member["GROUP"]
                )

                status = result.get("status")

                if status == "success":

                    created += 1

                elif status == "short_member":

                    skipped += 1

                else:

                    failed += 1

                    errors.append(
                        {
                            "member": member["MEMBER_ID"],
                            "profile": member["PROFILE"],
                            "result": result
                        }
                    )

            except Exception as ex:

                failed += 1

                errors.append(
                    {
                        "member": member.get(
                            "MEMBER_ID",
                            "UNKNOWN"
                        ),
                        "profile": member.get(
                            "PROFILE",
                            "UNKNOWN"
                        ),
                        "error": str(ex)
                    }
                )

        with open(
            r"C:\tekla-mcp\failed_members.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                errors,
                f,
                indent=4
            )

        profile_summary = {}

        for error in errors:

            profile = error.get(
                "profile",
                "UNKNOWN"
            )

            profile_summary[
                profile
            ] = (
                profile_summary.get(
                    profile,
                    0
                ) + 1
            )

        with open(
            r"C:\tekla-mcp\root_cause_report.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                profile_summary,
                f,
                indent=4
            )

        return {
            "status": "completed",
            "created": created,
            "failed": failed,
            "skipped": skipped,
            "total": len(members),
            "errors": errors
        }

    except Exception as ex:

        return {
            "status": "exception",
            "error": str(ex)
        }

# ----------------------------------------------------
# MAIN
# ----------------------------------------------------

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--test",
        action="store_true"
    )

    args = parser.parse_args()

    if args.test:

        print("Testing Tekla Connection...")

        print()

        print("Model Info:")
        print(get_model_info())

        print()

        print("Beam Count:")
        print(count_beams())

        print()

        print("Selected Count:")
        print(selected_count())

        print()

        print("Profiles:")
        print(
            list_beam_profiles_unique(200)
        )

        print()

        print("Create Test Beam: SKIPPED")

        print()

        print("STAAD Import Test:")

        result = import_staad_json(
            limit=0
        )

        print(result)

        with open(
            r"C:\tekla-mcp\failed_members.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                errors,
                f,
                indent=4
            )

        profile_summary = {}

        for error in errors:

            profile = error.get(
                "profile",
                "UNKNOWN"
            )

            profile_summary[
                profile
            ] = (
                profile_summary.get(
                    profile,
                    0
                ) + 1
            )

        with open(
            r"C:\tekla-mcp\root_cause_report.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                profile_summary,
                f,
                indent=4
            )

        profile_count = {}

        for err in result["errors"]:

            profile = err["profile"]

            profile_count[profile] = (
                profile_count.get(profile, 0) + 1
            )

        print()
        print("FAILURES BY PROFILE")

        for p, c in sorted(
            profile_count.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            print(f"{c:3}  {p}")

    else:

        print()
        print("===================================")
        print("Starting Tekla MCP Server...")
        print("===================================")
        print()

        try:

            mcp.run()

        except Exception as ex:

            print()
            print("===================================")
            print("MCP SERVER ERROR")
            print("===================================")
            print()

            print(str(ex))

            print()

            input("Press Enter to close...")

