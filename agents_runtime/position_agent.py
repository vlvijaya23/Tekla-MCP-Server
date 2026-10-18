"""
Steel AI Mind
Position Agent
"""


def get_position_rule(
    member_type,
    profile
):

    #
    # Columns
    #

    if member_type == "COLUMN":

        return {
            "plane": "MIDDLE",
            "depth": "MIDDLE",
            "rotation": "FRONT"
        }

    #
    # Beams
    #

    if member_type == "BEAM":

        return {
            "plane": "MIDDLE",
            "depth": "TOP",
            "rotation": "FRONT"
        }

    #
    # Angle Braces
    #

    if member_type == "ANGLE_BRACE":

        return {
            "plane": "MIDDLE",
            "depth": "CG",
            "rotation": "FRONT"
        }

    #
    # Braces
    #

    if member_type == "BRACE":

        return {
            "plane": "MIDDLE",
            "depth": "MIDDLE",
            "rotation": "FRONT"
        }

    #
    # Pipe Supports
    #

    if member_type == "PIPE_SUPPORT":

        return {
            "plane": "MIDDLE",
            "depth": "MIDDLE",
            "rotation": "FRONT"
        }

    #
    # Default
    #

    return {
        "plane": "MIDDLE",
        "depth": "MIDDLE",
        "rotation": "FRONT"
    }


if __name__ == "__main__":

    print(
        get_position_rule(
            "COLUMN",
            "HE220A"
        )
    )

    print(
        get_position_rule(
            "BEAM",
            "HE160A"
        )
    )

    print(
        get_position_rule(
            "ANGLE_BRACE",
            "L75*75*10"
        )
    )