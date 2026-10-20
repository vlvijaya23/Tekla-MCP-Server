import sys

sys.path.append(
    r"C:\TeklaAssistant"
)

from staad.std_parser import parse_staad
from staad.member_classifier import classify_all_members


class AnalysisController:

    def analyze_staad(
        self,
        std_file
    ):

        try:

            with open(
                std_file,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                lines = f.readlines()

            #
            # Parse STAAD
            #

            data = parse_staad(
                lines
            )

            #
            # Real geometry classification
            #

            classifications = (
                classify_all_members(
                    data
                )
            )

            #
            # Profiles
            #

            profiles = sorted(
                {
                    prop["profile"]
                    for prop in data["properties"]
                }
            )

            #
            # Results
            #

            result = {

                "members": len(
                    data["members"]
                ),

                "profiles": profiles,

                "mapped_profiles": len(
                    profiles
                ),

                "columns": len(
                    classifications.get(
                        "COLUMN",
                        []
                    )
                ),

                "beams": len(
                    classifications.get(
                        "BEAM",
                        []
                    )
                ),

                "braces": len(
                    classifications.get(
                        "BRACE",
                        []
                    )
                ),

                "nodes": len(
                    data["nodes"]
                ),

                "groups": len(
                    data["groups"]
                ),

                "properties": len(
                    data["properties"]
                ),

                "materials": 0
            }

            return result

        except Exception as ex:

            return {

                "members": 0,

                "profiles": [],

                "mapped_profiles": 0,

                "columns": 0,

                "beams": 0,

                "braces": 0,

                "nodes": 0,

                "groups": 0,

                "properties": 0,

                "error": str(ex)
            }