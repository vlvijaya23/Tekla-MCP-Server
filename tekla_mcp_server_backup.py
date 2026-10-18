"""
Tekla MCP Server
"""

import os
import sys
import pythonnet
import json

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
    Beam
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

PROFILE_MAP = {
    "HE220A": "HE220A",
    "HE160A": "HE160A",
    "UPN140": "UPN140",
    "L75X75X10": "L75*75*10",
    "L100X100X10": "L100*100*10",
    "100X6.3SHS": "SHS100*100*6.3"
}


def map_profile(profile):

    return PROFILE_MAP.get(
        profile,
        profile
    )

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
            start_x,
            start_y,
            start_z
        )

        beam.EndPoint = Point(
            end_x,
            end_y,
            end_z
        )

        beam.Profile.ProfileString = profile

        beam.Material.MaterialString = "S355"

        phase = phase.upper().strip()

        if phase in ["_COLUMN", "COLUMN"]:

            beam.Class = "3"

        elif phase in ["_TRAYCOLUMN", "TRAYCOLUMN"]:

            beam.Class = "8"

        elif phase == "PRIMARY_STEEL":

            beam.Class = "3"

        elif phase == "SECONDARY_STEEL":

            beam.Class = "8"

        elif phase == "BRACING":

            beam.Class = "5"

        elif phase == "PIPE_SUPPORT":

            beam.Class = "7"

        elif phase == "PLATE_GIRDER":

            beam.Class = "6"

        elif phase == "MONORAIL":

            beam.Class = "9"

        else:

            beam.Class = "4"

        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)
        dz = abs(end_z - start_z)

        horizontal = max(dx, dy)

        if dz > horizontal:

            beam.Name = f"COLUMN_{name}"

        elif horizontal > 0 and dz < (horizontal * 0.20):

            beam.Name = f"BEAM_{name}"

        else:

            beam.Name = f"BRACE_{name}"

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
    json_file: str = r"C:\TeklaAssistant\staad_payload.json",
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

                status = result.get(
                    "status"
                )

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

        print("Create Test Beam:")
        print(
            create_beam(
                profile="HW150*150*7*10",
                start_x=0,
                start_y=0,
                start_z=0,
                end_x=0,
                end_y=0,
                end_z=5000,
                name="TEST_BEAM"
            )
        )

        print()

        print("STAAD Import Test:")

        result = import_staad_json(
            limit=0
        )

        print(result)

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

