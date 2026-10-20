-"""
member_classifier.py

AI-ready structural member classifier.

Purpose:
    Determine whether a member is:

    - COLUMN
    - BEAM
    - BRACE
    - ANGLE_BRACE
    - PIPE_SUPPORT

Future:
    - LLM classification
    - STAAD beta angle analysis
    - Connection-based reasoning
    - Structural topology analysis
"""

import math


def classify_member(
    profile: str,
    start_x: float,
    start_y: float,
    start_z: float,
    end_x: float,
    end_y: float,
    end_z: float
):
    """
    Geometry-based classification.
    """

    dx = abs(end_x - start_x)
    dy = abs(end_y - start_y)
    dz = abs(end_z - start_z)

    horizontal = math.sqrt(
        dx ** 2 +
        dy ** 2
    )

    length = math.sqrt(
        dx ** 2 +
        dy ** 2 +
        dz ** 2
    )

    if length == 0:
        return "UNKNOWN"

    vertical_ratio = dz / length

    #
    # COLUMN
    #

    if vertical_ratio >= 0.90:
        return "COLUMN"

    #
    # PIPE SUPPORT
    #

    if profile.upper().startswith(
        "UPN"
    ):
        return "PIPE_SUPPORT"

    #
    # ANGLE BRACE
    #

    if profile.upper().startswith(
        "L"
    ):
        return "ANGLE_BRACE"

    #
    # BRACE
    #

    if (
        horizontal > 0.0
        and dz > 0.0
    ):
        return "BRACE"

    #
    # BEAM
    #

    return "BEAM"


def get_material(
    profile: str
):
    """
    Material assignment.
    """

    return "S355"


def get_class(
    member_type: str
):
    """
    Tekla class assignment.
    """

    class_map = {
        "COLUMN": "2",
        "BEAM": "3",
        "BRACE": "4",
        "ANGLE_BRACE": "5",
        "PIPE_SUPPORT": "6"
    }

    return class_map.get(
        member_type,
        "3"
    )


def get_phase(
    member_type: str
):
    """
    Construction phase.
    """

    phase_map = {
        "COLUMN": "PRIMARY",
        "BEAM": "PRIMARY",
        "BRACE": "SECONDARY",
        "ANGLE_BRACE": "SECONDARY",
        "PIPE_SUPPORT": "SECONDARY"
    }

    return phase_map.get(
        member_type,
        "PRIMARY"
    )


def get_member_name(
    member_type: str
):
    """
    Display name.
    """

    name_map = {
        "COLUMN": "COLUMN",
        "BEAM": "BEAM",
        "BRACE": "BEAM",
        "ANGLE_BRACE": "BEAM",
        "PIPE_SUPPORT": "BEAM"
    }

    return name_map.get(
        member_type,
        "BEAM"
    )


def process_member(
    profile: str,
    start_x: float,
    start_y: float,
    start_z: float,
    end_x: float,
    end_y: float,
    end_z: float
):
    """
    Main classification entry point.
    """

    member_type = classify_member(
        profile,
        start_x,
        start_y,
        start_z,
        end_x,
        end_y,
        end_z
    )

    return {
        "name": get_member_name(
            member_type
        ),
        "classification": {
            "member_type": member_type,
            "material": get_material(
                profile
            ),
            "class": get_class(
                member_type
            ),
            "phase": get_phase(
                member_type
            )
        }
    }