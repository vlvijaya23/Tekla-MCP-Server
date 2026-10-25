import json

from Tekla.Structures.Model import (
    Beam
)

from Tekla.Structures.Geometry3d import (
    Point
)

# PATCH_START_BEAM_MERGER

def merge_all_safe_beam_chains(
    model,
    beam_chains
):

    merged_count = 0

    for chain in beam_chains:

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

        points = []

        for beam in members:

            points.append(
                beam.StartPoint
            )

            points.append(
                beam.EndPoint
            )

        start_point = min(
            points,
            key=lambda p: (
                p.X,
                p.Y,
                p.Z
            )
        )

        end_point = max(
            points,
            key=lambda p: (
                p.X,
                p.Y,
                p.Z
            )
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
        "status":
            "merged_all_beams",

        "chains":
            merged_count
    }

# PATCH_END_BEAM_MERGER