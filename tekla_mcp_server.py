"""
Tekla MCP Server
"""

import os
import sys
import pythonnet

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
    ModelObject
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
def list_beam_profiles(limit: int = 10):

    model = get_model()

    selector = model.GetModelObjectSelector()

    beams = selector.GetAllObjectsWithType(
        ModelObject.ModelObjectEnum.BEAM
    )

    profiles = []

    while beams.MoveNext():

        beam = beams.Current

        try:

            profiles.append(
                beam.Profile.ProfileString
            )

        except Exception:
            pass

        if len(profiles) >= limit:
            break

    return profiles


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