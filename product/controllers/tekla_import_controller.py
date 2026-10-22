import json
import sys

sys.path.append(
    r"C:\TeklaAssistant\staad"
)

from staad_payload_builder_json import (
    build_payload
)

from product.controllers.tekla_bridge import (
    TeklaBridge
)


class TeklaImportController:

    def __init__(self):

        self.bridge = (
            TeklaBridge()
        )

    def create_model(
        self,
        std_file,
        progress_callback=None
    ):

        payload = build_payload(
            std_file
        )

        if progress_callback:

            progress_callback(
                25
            )

        output_file = (
            r"C:\TeklaAssistant\data\staad_payload.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                payload,
                f,
                indent=4
            )

        if progress_callback:

            progress_callback(
                50
            )

        tekla_result = (
            self.bridge.import_payload(
                output_file,
                progress_callback
            )
        )

        if progress_callback:

            progress_callback(
                100
            )

        return {

            "payload_file": output_file,

            "members":
                payload["payload_count"],

            "tekla":
                tekla_result
        }