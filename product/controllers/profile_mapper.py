PROFILE_MAP = {

    "HE160A": "HEA160",

    "HE220A": "HEA220",

    "UPN140": "UPN140",

    "L75X75X10": "L75*75*10",

    "L100X100X10": "L100*100*10",

    "100X6.3SHS": "SHS100*100*6.3"
}


def map_profile(
    staad_profile
):

    return PROFILE_MAP.get(
        staad_profile,
        "REVIEW_REQUIRED"
    )