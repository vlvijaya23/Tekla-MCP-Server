import os
import sys
import pythonnet

TEKLA_BIN = r"C:\TeklaStructures\2025.0\bin"

sys.path.append(TEKLA_BIN)

pythonnet.load("netfx")

import clr

clr.AddReference(
    os.path.join(
        TEKLA_BIN,
        "Tekla.Structures.Model.dll"
    )
)

from Tekla.Structures.Model import Beam

beam = Beam()

print("PLANE ENUM")
print("=" * 30)

for item in beam.Position.PlaneEnum.GetNames(
    beam.Position.PlaneEnum
):
    print(item)

print()
print("DEPTH ENUM")
print("=" * 30)

for item in beam.Position.DepthEnum.GetNames(
    beam.Position.DepthEnum
):
    print(item)

print()
print("ROTATION ENUM")
print("=" * 30)

for item in beam.Position.RotationEnum.GetNames(
    beam.Position.RotationEnum
):
    print(item)