"""
Steel AI Mind
Topology Agent
"""


def detect_member_role(
    member_type,
    length
):

    if member_type == "COLUMN":

        return "CONTINUOUS_COLUMN"

    if member_type == "BEAM":

        return "CONTINUOUS_BEAM"

    if "BRACE" in member_type:

        return "BRACE_CONNECTION"

    return "GENERAL_MEMBER"


if __name__ == "__main__":

    print(
        detect_member_role(
            "COLUMN",
            6.5
        )
    )

    print(
        detect_member_role(
            "BEAM",
            9.2
        )
    )

    print(
        detect_member_role(
            "ANGLE_BRACE",
            2.8
        )
    )