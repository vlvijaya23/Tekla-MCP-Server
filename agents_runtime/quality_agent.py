"""
Steel AI Mind
Quality Agent
"""

from classification_agent import classify_member


def evaluate_member(
    profile,
    start_x,
    start_y,
    start_z,
    end_x,
    end_y,
    end_z
):

    info = classify_member(
        profile,
        start_x,
        start_y,
        start_z,
        end_x,
        end_y,
        end_z
    )

    score = 100

    warnings = []

    #
    # very short members
    #

    if info["length"] < 0.50:

        score -= 15

        warnings.append(
            "Very short member"
        )

    #
    # angle brace review
    #

    if info["member_type"] == "ANGLE_BRACE":

        warnings.append(
            "Check CG alignment"
        )

    #
    # brace review
    #

    if "BRACE" in info["member_type"]:

        warnings.append(
            "Verify brace end connections"
        )

    #
    # beam review
    #

    if info["member_type"] == "BEAM":

        warnings.append(
            "Verify beam-column intersection"
        )

    return {
        "member_type": info["member_type"],
        "score": score,
        "warnings": warnings
    }


if __name__ == "__main__":

    result = evaluate_member(
        profile="L75*75*10",
        start_x=0,
        start_y=0,
        start_z=0,
        end_x=5,
        end_y=5,
        end_z=0
    )

    print(result)