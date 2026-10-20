import json
import os


class ProfileLearningEngine:

    FILE = (
        r"C:\tekla-mcp\product\data\profile_learning.json"
    )

    def load(self):

        if not os.path.exists(
            self.FILE
        ):

            return {}

        with open(
            self.FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def find_mapping(
        self,
        profile
    ):

        data = self.load()

        return data.get(
            profile
        )

    def save_mapping(
        self,
        staad_profile,
        tekla_profile
    ):

        data = self.load()

        data[
            staad_profile
        ] = tekla_profile

        with open(
            self.FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )