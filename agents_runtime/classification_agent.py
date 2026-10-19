"""
Steel AI Mind
Classification Agent
"""

import math


def classify_member(
    profile,
    start_x,
    start_y,
    start_z,
    end_x,
    end_y,
    end_z
):

    dx = abs(end_x - start_x)
    dy = abs(end_y - start_y)
    dz = abs(end_z - start_z)

    horizontal = max(dx, dz)

    length = math.sqrt(
        dx ** 2 +
        dy ** 2 +
        dz ** 2
    )

    result = {
        "member_type": "UNKNOWN",
        "class": "4",
        "phase": "PRIMARY_STEEL",
        "material": "S355",
        "position_rule": "MIDDLE",
        "length": round(length, 3)
    }

    #
    # COLUMN
    #

    if dy > horizontal:

        result["member_type"] = "COLUMN"
        result["class"] = "3"
        result["phase"] = "PRIMARY_STEEL"
        result["position_rule"] = "MIDDLE"

        return result

    #
    # ANGLE BRACE
    #

    if profile.startswith("L"):

        result["member_type"] = "ANGLE_BRACE"
        result["class"] = "5"
        result["phase"] = "BRACING"
        result["position_rule"] = "CG"

        return result

    #
    # CHANNEL SUPPORT
    #

    if profile.startswith("UPN"):

        result["member_type"] = "PIPE_SUPPORT"
        result["class"] = "7"
        result["phase"] = "PIPE_SUPPORT"
        result["position_rule"] = "MIDDLE"

        return result

    #
    # SHS / RHS
    #

    if (
        profile.startswith("SHS")
        or
        profile.startswith("RHS")
    ):

        result["member_type"] = "TUBE_MEMBER"
        result["class"] = "3"
        result["phase"] = "PRIMARY_STEEL"
        result["position_rule"] = "CG"

        return result

    #
    # BEAM
    #

    if (
        horizontal > 0
        and
        dz < horizontal * 0.20
    ):

        result["member_type"] = "BEAM"
        result["class"] = "3"
        result["phase"] = "PRIMARY_STEEL"
        result["position_rule"] = "TOP"

        return result

    #
    # GENERAL BRACE
    #

    result["member_type"] = "BRACE"
    result["class"] = "5"
    result["phase"] = "BRACING"
    result["position_rule"] = "MIDDLE"

    return result


if __name__ == "__main__":

    test = classify_member(
        profile="L75*75*10",
        start_x=0,
        start_y=0,
        start_z=0,
        end_x=5,
        end_y=5,
        end_z=0
    )

    print(test)