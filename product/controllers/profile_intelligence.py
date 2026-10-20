import re
from difflib import SequenceMatcher

from product.controllers.profile_learning_engine import (
    ProfileLearningEngine
)

class ProfileIntelligence:

    def __init__(self):

        self.learning = (
            ProfileLearningEngine()
        )

    def normalize(
        self,
        profile
    ):

        if not profile:
            return ""

        profile = profile.upper()

        profile = profile.replace(
            " ",
            ""
        )

        profile = profile.replace(
            "*",
            ""
        )

        profile = profile.replace(
            "X",
            ""
        )

        return profile

    def confidence(
        self,
        a,
        b
    ):

        return round(
            SequenceMatcher(
                None,
                a,
                b
            ).ratio() * 100,
            1
        )

    def infer_mapping(
        self,
        staad_profile
    ):

        profile = (
            staad_profile.upper()
        )

        learned = (
            self.learning.find_mapping(
                profile
            )
        )

        if learned:

            return {
                "tekla": learned,
                "confidence": 100.0,
                "reason": "Learned mapping"
            }

        #
        # HE Sections
        #

        match = re.match(
            r"HE(\d+)A",
            profile
        )

        if match:

            size = match.group(1)

            return {
                "tekla": f"HEA{size}",
                "confidence": 99.0,
                "reason": "HE section match"
            }

        #
        # UPN
        #

        match = re.match(
            r"UPN(\d+)",
            profile
        )

        if match:

            return {
                "tekla": profile,
                "confidence": 100.0,
                "reason": "Direct UPN match"
            }

        #
        # Angle
        #

        match = re.match(
            r"L(\d+)X(\d+)X(\d+)",
            profile
        )

        if match:

            a = match.group(1)
            b = match.group(2)
            c = match.group(3)

            return {
                "tekla": f"L{a}*{b}*{c}",
                "confidence": 99.0,
                "reason": "Angle conversion"
            }

        #
        # SHS
        #

        match = re.match(
            r"(\d+)X([\d\.]+)SHS",
            profile
        )

        if match:

            size = match.group(1)
            thk = match.group(2)

            return {
                "tekla": (
                    f"SHS{size}*{size}*{thk}"
                ),
                "confidence": 95.0,
                "reason": "SHS conversion"
            }

        #
        # Tube Profiles
        #

        if (
            "TUBE" in profile
            or
            "PIPE" in profile
        ):

            return {
                "tekla": "REVIEW_REQUIRED",
                "confidence": 50.0,
                "reason": "Tube profile requires review"
            }

        #
        # Unknown
        #

        return {
            "tekla": "REVIEW_REQUIRED",
            "confidence": 0.0,
            "reason": "Unknown profile"
        }