"""
Steel AI Mind
Naming Agent
"""

def generate_name(
    member_type,
    member_id
):

    prefixes = {
        "COLUMN": "COL",
        "BEAM": "BM",
        "BRACE": "BR",
        "ANGLE_BRACE": "AB",
        "PIPE_SUPPORT": "PS",
        "TUBE_MEMBER": "TM"
    }

    prefix = prefixes.get(
        member_type,
        "ST"
    )

    return f"{prefix}-{member_id:04d}"


if __name__ == "__main__":

    print(
        generate_name(
            "COLUMN",
            7
        )
    )

    print(
        generate_name(
            "BEAM",
            100
        )
    )

    print(
        generate_name(
            "ANGLE_BRACE",
            79
        )
    )