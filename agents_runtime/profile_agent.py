import json

FAILED_FILE = r"C:\tekla-mcp\failed_members.json"

REPORT_FILE = r"C:\tekla-mcp\profile_recovery_report.json"


PROFILE_RECOVERY_MAP = {
    "L75X75X10": "L75*75*10",
    "L100X100X10": "L100*100*10",
    "100X6.3SHS": "SHS100*100*6.3",
    "TUBE TH 0.012 WT 0.22 DT 0.21": "REVIEW_REQUIRED",
    "TUBE TH 0.01 WT 0.16 DT 0.152": "REVIEW_REQUIRED"
}


def main():

    with open(
        FAILED_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        failures = json.load(f)

    report = []

    print()
    print("PROFILE RECOVERY REPORT")
    print("=======================")

    for item in failures:

        profile = item["profile"]

        recommendation = PROFILE_RECOVERY_MAP.get(
            profile,
            "NO_MAPPING_FOUND"
        )

        report.append(
            {
                "profile": profile,
                "recommendation": recommendation
            }
        )

        print(
            f"{profile} -> {recommendation}"
        )

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
    print(
        f"Recommendations Generated : {len(report)}"
    )


if __name__ == "__main__":

    main()