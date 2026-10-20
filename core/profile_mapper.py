"""
profile_mapper.py

STAAD → Tekla profile mapping engine

Future Enhancements:
- Auto Tekla catalog lookup
- AI profile matching
- User mapping database
- Profile validation
"""

from typing import Dict


PROFILE_MAP: Dict[str, str] = {
    # HE Sections
    "HE160A": "HEA160",
    "HE220A": "HEA220",

    # Channels
    "UPN140": "UPN140",

    # Angles
    "L75X75X10": "L75*75*10",
    "L100X100X10": "L100*100*10",

    # Hollow Sections
    "100X6.3SHS": "SHS100*100*6.3",
}


def map_profile(profile: str) -> str:
    """
    Convert STAAD profile to Tekla profile.

    Example:
        HE160A      -> HEA160
        HE220A      -> HEA220
        L75X75X10   -> L75*75*10

    Parameters
    ----------
    profile : str
        STAAD profile

    Returns
    -------
    str
        Tekla profile
    """

    if not profile:
        return ""

    profile = profile.strip()

    return PROFILE_MAP.get(
        profile,
        profile
    )


def profile_exists(profile: str) -> bool:
    """
    Check whether profile is present
    in current mapping table.
    """

    return profile in PROFILE_MAP


def add_profile_mapping(
    staad_profile: str,
    tekla_profile: str
) -> None:
    """
    Add profile mapping dynamically.
    """

    PROFILE_MAP[
        staad_profile.strip()
    ] = tekla_profile.strip()


def get_all_mappings() -> Dict[str, str]:
    """
    Return complete mapping table.
    """

    return dict(PROFILE_MAP)


def print_mapping_report() -> None:
    """
    Debug report.
    """

    print("\nPROFILE MAPPINGS")
    print("-" * 40)

    for staad, tekla in sorted(
        PROFILE_MAP.items()
    ):
        print(
            f"{staad:<20} -> {tekla}"
        )