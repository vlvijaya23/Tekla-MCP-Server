import json

from Tekla.Structures.Model import (
    ModelObject
)

# PATCH_START_COLUMN_DETECTOR

def detect_selected_split_columns(
    model
):

    selector = (
        model.GetModelObjectSelector()
    )

    objects = (
        selector.GetAllObjectsWithType(
            ModelObject.ModelObjectEnum.BEAM
        )
    )

    columns = []

    while objects.MoveNext():

        try:

            beam = objects.Current

            if (
                beam.Name.upper()
                != "COLUMN"
            ):
                continue

            columns.append(
                {
                    "id":
                        beam.Identifier.ID,

                    "profile":
                        beam.Profile.ProfileString,

                    "start_x":
                        beam.StartPoint.X,

                    "start_y":
                        beam.StartPoint.Y,

                    "start_z":
                        beam.StartPoint.Z,

                    "end_x":
                        beam.EndPoint.X,

                    "end_y":
                        beam.EndPoint.Y,

                    "end_z":
                        beam.EndPoint.Z
                }
            )

        except Exception:
            pass

    chains = []
    used = set()

    for column in columns:

        if column["id"] in used:
            continue

        chain = [column]

        changed = True

        while changed:

            changed = False

            for candidate in columns:

                if candidate["id"] in used:
                    continue

                if (
                    candidate["id"]
                    ==
                    chain[0]["id"]
                ):
                    continue

                for existing in chain:

                    same_profile = (
                        existing["profile"]
                        ==
                        candidate["profile"]
                    )

                    x1 = (
                        existing["start_x"]
                        +
                        existing["end_x"]
                    ) / 2

                    x2 = (
                        candidate["start_x"]
                        +
                        candidate["end_x"]
                    ) / 2

                    y1 = (
                        existing["start_y"]
                        +
                        existing["end_y"]
                    ) / 2

                    y2 = (
                        candidate["start_y"]
                        +
                        candidate["end_y"]
                    ) / 2

                    same_x = (
                        abs(x1 - x2)
                        < 50
                    )

                    same_y = (
                        abs(y1 - y2)
                        < 50
                    )

                    connected = (
                        abs(
                            existing["end_z"]
                            -
                            candidate["start_z"]
                        )
                        < 500
                        or
                        abs(
                            candidate["end_z"]
                            -
                            existing["start_z"]
                        )
                        < 500
                    )

                    if (
                        same_profile
                        and same_x
                        and same_y
                        and connected
                    ):

                        chain.append(
                            candidate
                        )

                        used.add(
                            candidate["id"]
                        )

                        changed = True

                        break

                if changed:
                    break

        if len(chain) > 1:

            chain_ids = sorted(
                [
                    member["id"]
                    for member in chain
                ]
            )

            min_z = min(
                [
                    min(
                        member["start_z"],
                        member["end_z"]
                    )
                    for member in chain
                ]
            )

            max_z = max(
                [
                    max(
                        member["start_z"],
                        member["end_z"]
                    )
                    for member in chain
                ]
            )

            chains.append(
                {
                    "type":
                        "COLUMN_CHAIN",

                    "profile":
                        chain[0]["profile"],

                    "members":
                        chain_ids,

                    "segment_count":
                        len(chain_ids),

                    "length":
                        round(
                            max_z - min_z,
                            0
                        ),

                    "status":
                        "SAFE"
                }
            )

            for member in chain:

                used.add(
                    member["id"]
                )

    with open(
        r"C:\tekla-mcp\column_chains.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chains,
            f,
            indent=4
        )

    return chains

# PATCH_END_COLUMN_DETECTOR