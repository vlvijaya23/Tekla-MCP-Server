import json

from Tekla.Structures.Model import (
    Beam,
    ModelObject
)

from Tekla.Structures.Geometry3d import (
    Point
)


def get_beam_by_id(
    model,
    object_id
):

    selector = (
        model.GetModelObjectSelector()
    )

    objects = (
        selector.GetAllObjectsWithType(
            ModelObject.ModelObjectEnum.BEAM
        )
    )

    while objects.MoveNext():

        beam = objects.Current

        if (
            beam.Identifier.ID
            == object_id
        ):
            return beam

    return None

# PATCH_START_COLUMN_MERGER

def merge_safe_column_chains(
    model
):

    with open(
        r"C:\tekla-mcp\column_chains.json",
        "r",
        encoding="utf-8"
    ) as f:

        chains = json.load(f)

    if not chains:

        return {
            "status": "no_chains"
        }

    merged_count = 0

    for chain in chains:

        if (
            chain["status"]
            != "SAFE"
        ):
            continue

        members = []

        for member_id in chain["members"]:

            beam = get_beam_by_id(
                model,
                member_id
            )

            if beam:

                members.append(
                    beam
                )

        if len(members) < 2:
            continue

        start_point = min(
            [
                p
                for beam in members
                for p in [
                    beam.StartPoint,
                    beam.EndPoint
                ]
            ],
            key=lambda p: p.Z
        )

        end_point = max(
            [
                p
                for beam in members
                for p in [
                    beam.StartPoint,
                    beam.EndPoint
                ]
            ],
            key=lambda p: p.Z
        )

        merged = Beam()

        merged.StartPoint = Point(
            start_point.X,
            start_point.Y,
            start_point.Z
        )

        merged.EndPoint = Point(
            end_point.X,
            end_point.Y,
            end_point.Z
        )

        merged.Profile.ProfileString = (
            members[0].Profile.ProfileString
        )

        merged.Material.MaterialString = (
            members[0].Material.MaterialString
        )

        merged.Class = (
            members[0].Class
        )

        merged.Name = (
            members[0].Name
        )

        merged.Position.Plane = (
            members[0].Position.Plane
        )

        merged.Position.Rotation = (
            members[0].Position.Rotation
        )

        merged.Position.Depth = (
            members[0].Position.Depth
        )

        if not merged.Insert():
            continue

        model.CommitChanges()

        for beam in members:
            beam.Delete()

        model.CommitChanges()

        merged_count += 1

    return {
        "status": "merged_all",
        "chains": merged_count
    }

# PATCH_END_COLUMN_MERGER