import json
from collections import Counter

FAILED_FILE = r"C:\tekla-mcp\failed_members.json"

REPORT_FILE = r"C:\tekla-mcp\root_cause_report.json"


def main():

    with open(
        FAILED_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        failures = json.load(f)

    profile_counter = Counter()

    for item in failures:

        profile_counter[
            item["profile"]
        ] += 1

    report = {
        "total_failures": len(failures),
        "profiles": dict(profile_counter)
    }

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4
        )

    print()
    print("GEOMETRY AGENT REPORT")
    print("====================")

    for profile, count in profile_counter.items():

        print(
            f"{profile} : {count}"
        )

    print()
    print(
        f"Total Failures : {len(failures)}"
    )


if __name__ == "__main__":

    main()