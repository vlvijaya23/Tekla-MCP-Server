import os
import sys

BASE_DIR = r"C:\tekla-mcp"

if BASE_DIR not in sys.path:
    sys.path.insert(
        0,
        BASE_DIR
    )

from tekla_mcp_server import (
    import_staad_json
)


class TeklaBridge:

    def import_payload(
        self,
        payload_file
    ):

        result = import_staad_json(
            json_file=payload_file,
            limit=0
        )

        return result