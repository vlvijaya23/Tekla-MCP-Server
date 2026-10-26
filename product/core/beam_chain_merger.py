import json

from Tekla.Structures.Model import (
    Beam,
    ModelObject
)

from Tekla.Structures.Geometry3d import (
    Point
)

# PATCH_START_BEAM_MERGER

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


def merge_beam_chain(
    model,
    member_ids
):

    members = []

    for member_id in member_ids:

        beam = get_beam_by_id(
            model,
            member_id
        )

        if beam:

            members.append(
                beam
            )

    if len(members) < 2:

        return {
            "status":
                "not_enough_members"
        }

    points = []

    for beam in members:

        points.append(
            beam.StartPoint
        )

        points.append(
            beam.EndPoint
        )

    max_distance = 0

    start_point = None
    end_point = None

    for p1 in points:

        for p2 in points:

            dx = (
                p2.X - p1.X
            )

            dy = (
                p2.Y - p1.Y
            )

            dz = (
                p2.Z - p1.Z
            )

            distance = (
                dx * dx +
                dy * dy +
                dz * dz
            ) ** 0.5

            if (
                distance
                >
                max_distance
            ):

                max_distance = distance

                start_point = p1
                end_point = p2

    if (
        start_point is None
        or
        end_point is None
    ):

        return {
            "status":
                "invalid_chain"
        }

    if max_distance < 1:

        return {
            "status":
                "invalid_chain"
        }

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

    try:

        success = merged.Insert()

    except Exception as ex:

        print(
            "BEAM INSERT FAILED:",
            str(ex)
        )

        return {
            "status":
                "insert_failed"
        }

    if not success:

        return {
            "status":
                "insert_failed"
        }

    model.CommitChanges()

    for beam in members:

        try:

            beam.Delete()

        except Exception:

            pass

    model.CommitChanges()

    return {
        "status":
            "merged",

        "new_id":
            merged.Identifier.ID,

        "deleted":
            len(members)
    }


def merge_all_safe_beam_chains(
    model,
    beam_chains
):

    merged_count = 0

    skipped_count = 0

    for chain in beam_chains:

        try:

            result = merge_beam_chain(
                model,
                chain["members"]
            )

            if (
                result.get(
                    "status"
                )
                ==
                "merged"
            ):

                merged_count += 1

            else:

                skipped_count += 1

        except Exception as ex:

            print(
                "BEAM MERGE FAILED:",
                str(ex)
            )

            skipped_count += 1

    return {
        "status":
            "merged_all_beams",

        "chains":
            merged_count,

        "skipped":
            skipped_count
    }
# PATCH_END_BEAM_MERGER
