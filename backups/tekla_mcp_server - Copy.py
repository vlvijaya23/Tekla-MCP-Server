"""
Tekla MCP Server - Minimal Loader Test
"""

import os
import sys
import pythonnet

# ----------------------------------------------------
# Tekla installation
# ----------------------------------------------------

TEKLA_BIN = r"C:\TeklaStructures\2025.0\bin"

if not os.path.exists(TEKLA_BIN):
    raise Exception(
        f"Tekla bin folder not found: {TEKLA_BIN}"
    )

sys.path.append(TEKLA_BIN)

# ----------------------------------------------------
# Load .NET Framework runtime
# ----------------------------------------------------

pythonnet.load("netfx")

import clr

# ----------------------------------------------------
# Load Tekla assemblies
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
# Tekla imports
# ----------------------------------------------------

from Tekla.Structures.Model import (
    Model,
    Beam,
    Position
)

print("Tekla assemblies loaded successfully")

# ----------------------------------------------------
# Connection test
# ----------------------------------------------------

model = Model()

if model.GetConnectionStatus():
    print("Connected to Tekla model")
else:
    print("Tekla running, but no model connection")