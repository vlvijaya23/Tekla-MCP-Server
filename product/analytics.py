import json
import os

from datetime import datetime


ANALYTICS_FILE = (
    r"C:\tekla-mcp\analytics.json"
)


def log_event(
    event_name
):

    if os.path.exists(
        ANALYTICS_FILE
    ):

        with open(
            ANALYTICS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(
                f
            )

    else:

        data = []

    data.append(
        {
            "event": event_name,
            "timestamp": str(
                datetime.now()
            )
        }
    )

    with open(
        ANALYTICS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


def get_summary():

    if not os.path.exists(
        ANALYTICS_FILE
    ):

        return {
            "starts": 0,
            "analyses": 0,
            "imports": 0,
            "success_rate": 0
        }

    with open(
        ANALYTICS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(
            f
        )

    starts = len(
        [
            x
            for x in data
            if x["event"]
            == "APPLICATION_STARTED"
        ]
    )

    analyses = len(
        [
            x
            for x in data
            if x["event"]
            == "ANALYZE_MODEL"
        ]
    )

    imports = len(
        [
            x
            for x in data
            if x["event"]
            == "CREATE_MODEL"
        ]
    )

    success_rate = 0

    if imports > 0:

        success_rate = 100

    return {
        "starts": starts,
        "analyses": analyses,
        "imports": imports,
        "success_rate": success_rate
    }