from Tekla.Structures.Model import (
    ModelObject
)


def column_exists_between(
    model,
    beam_a,
    beam_b,
    tolerance=100
):

    selector = (
        model.GetModelObjectSelector()
    )

    objects = (
        selector.GetAllObjectsWithType(
            ModelObject.ModelObjectEnum.BEAM
        )
    )

    min_x = min(
        beam_a["start_x"],
        beam_a["end_x"],
        beam_b["start_x"],
        beam_b["end_x"]
    )

    max_x = max(
        beam_a["start_x"],
        beam_a["end_x"],
        beam_b["start_x"],
        beam_b["end_x"]
    )

    min_y = min(
        beam_a["start_y"],
        beam_a["end_y"],
        beam_b["start_y"],
        beam_b["end_y"]
    )

    max_y = max(
        beam_a["start_y"],
        beam_a["end_y"],
        beam_b["start_y"],
        beam_b["end_y"]
    )

    while objects.MoveNext():

        try:

            part = objects.Current

            if (
                part.Name.upper()
                != "COLUMN"
            ):
                continue

            cx = (
                part.StartPoint.X
                +
                part.EndPoint.X
            ) / 2

            cy = (
                part.StartPoint.Y
                +
                part.EndPoint.Y
            ) / 2

            inside_x = (
                cx > min_x + tolerance
                and
                cx < max_x - tolerance
            )

            inside_y = (
                cy >= min_y - tolerance
                and
                cy <= max_y + tolerance
            )

            if (
                inside_x
                and
                inside_y
            ):
                return True

        except Exception:

            pass

    return False