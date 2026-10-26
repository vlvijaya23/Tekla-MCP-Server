from Tekla.Structures.Model import (
    Beam
)

from Tekla.Structures.Geometry3d import (
    Point
)

from product.core.beam_span_builder import (
    build_beam_spans
)


DEFAULT_PROFILE = "HEA160"
DEFAULT_MATERIAL = "S355"


def create_span_beams(
    model
):

    spans = build_beam_spans(
        model
    )

    created = 0

    for item in spans:

        span = item["span"]

        beams = item["beams"]

        profile = DEFAULT_PROFILE

        material = DEFAULT_MATERIAL

        beam_y = span["y"]

        beam_z = span["z"]

        if len(beams) > 0:

            source = beams[0]

            profile = source.get(
                "profile",
                DEFAULT_PROFILE
            )

            beam_y = (
                source["start_y"]
                +
                source["end_y"]
            ) / 2

            beam_z = (
                source["start_z"]
                +
                source["end_z"]
            ) / 2

        new_beam = Beam()

        new_beam.StartPoint = Point(
            span["start_x"],
            beam_y,
            beam_z
        )

        new_beam.EndPoint = Point(
            span["end_x"],
            beam_y,
            beam_z
        )

        new_beam.Profile.ProfileString = (
            profile
        )

        new_beam.Material.MaterialString = (
            material
        )

        new_beam.Name = (
            "STAAD_SPAN_BEAM"
        )

        if new_beam.Insert():

            created += 1

            print(
                "CREATED:",
                round(
                    span["length"],
                    0
                ),
                "PROFILE:",
                profile
            )

    model.CommitChanges()

    return {
        "status":
            "created",

        "count":
            created
    }