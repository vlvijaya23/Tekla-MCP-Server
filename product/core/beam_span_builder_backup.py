from Tekla.Structures.Model import (
    ModelObject
)


def get_columns(
    model
):

    columns = []

    selector = (
        model.GetModelObjectSelector()
    )

    objects = (
        selector.GetAllObjectsWithType(
            ModelObject.ModelObjectEnum.BEAM
        )
    )

    while objects.MoveNext():

        try:

            part = objects.Current

            if (
                part.Name.upper()
                != "COLUMN"
            ):
                continue

            height = abs(
                part.EndPoint.Z
                -
                part.StartPoint.Z
            )

            if height < 5000:
                continue

            columns.append(
                {
                    "id":
                        part.Identifier.ID,

                    "x":
                        (
                            part.StartPoint.X
                            +
                            part.EndPoint.X
                        ) / 2,

                    "y":
                        (
                            part.StartPoint.Y
                            +
                            part.EndPoint.Y
                        ) / 2,

                    "z":
                        min(
                            part.StartPoint.Z,
                            part.EndPoint.Z
                        ),

                    "height":
                        height
                }
            )

        except Exception:

            pass

    return columns

def get_beams(
    model
):

    beams = []

    selector = (
        model.GetModelObjectSelector()
    )

    objects = (
        selector.GetAllObjectsWithType(
            ModelObject.ModelObjectEnum.BEAM
        )
    )

    while objects.MoveNext():

        try:

            part = objects.Current

            if (
                part.Name.upper()
                == "COLUMN"
            ):
                continue

            beams.append(
                {
                    "id":
                        part.Identifier.ID,

                    "profile":
                        part.Profile.ProfileString,

                    "start_x":
                        part.StartPoint.X,

                    "start_y":
                        part.StartPoint.Y,

                    "start_z":
                        part.StartPoint.Z,

                    "end_x":
                        part.EndPoint.X,

                    "end_y":
                        part.EndPoint.Y,

                    "end_z":
                        part.EndPoint.Z
                }
            )

        except Exception:

            pass

    return beams


def build_spans(
    columns,
    y_tolerance=100,
    z_tolerance=100
):

    spans = []

    rows = {}

    for column in columns:

        row_key = (
            round(
                column["y"] / y_tolerance
            ),
            round(
                column["z"] / z_tolerance
            )
        )

        if row_key not in rows:

            rows[row_key] = []

        rows[row_key].append(
            column
        )

    for row_columns in rows.values():

        row_columns = sorted(
            row_columns,
            key=lambda c: c["x"]
        )

        for i in range(
            len(row_columns) - 1
        ):

            left = row_columns[i]

            right = row_columns[i + 1]

            length = abs(
                right["x"]
                -
                left["x"]
            )

            if length < 100:
                continue

            spans.append(
                {
                    "start_column":
                        left["id"],

                    "end_column":
                        right["id"],

                    "start_x":
                        left["x"],

                    "end_x":
                        right["x"],

                    "y":
                        left["y"],

                    "z":
                        left["z"],

                    "length":
                        length
                }
            )

    return spans

def assign_beams_to_spans(
    beams,
    spans,
    tolerance=100
):

    results = []

    for span in spans:

        span_beams = []

        for beam in beams:

            beam_x1 = min(
                beam["start_x"],
                beam["end_x"]
            )

            beam_x2 = max(
                beam["start_x"],
                beam["end_x"]
            )

            beam_y = (
                beam["start_y"]
                +
                beam["end_y"]
            ) / 2

            beam_z = (
                beam["start_z"]
                +
                beam["end_z"]
            ) / 2

            same_row = (
                abs(
                    beam_y
                    -
                    span["y"]
                )
                < tolerance
            )

            same_level = (
                abs(
                    beam_z
                    -
                    span["z"]
                )
                < tolerance
            )

            inside_span = (
                beam_x1
                >=
                span["start_x"]
                - tolerance
                and
                beam_x2
                <=
                span["end_x"]
                + tolerance
            )

            if (
                same_row
                and same_level
                and inside_span
            ):

                span_beams.append(
                    beam
                )

        results.append(
            {
                "span":
                    span,

                "beams":
                    span_beams
            }
        )

    return results


def build_beam_spans(
    model
):

    columns = get_columns(
        model
    )

    beams = get_beams(
        model
    )

    spans = build_spans(
        columns
    )

    return assign_beams_to_spans(
        beams,
        spans
    )

def debug_span_columns(
    model
):

    columns = get_columns(
        model
    )

    spans = build_spans(
        columns
    )

    result = []

    for span in spans:

        result.append(
            {
                "length":
                    round(
                        span["length"],
                        0
                    ),

                "start_x":
                    round(
                        span["start_x"],
                        0
                    ),

                "end_x":
                    round(
                        span["end_x"],
                        0
                    ),

                "y":
                    round(
                        span["y"],
                        0
                    ),

                "start_column":
                    span["start_column"],

                "end_column":
                    span["end_column"]
            }
        )

    return result