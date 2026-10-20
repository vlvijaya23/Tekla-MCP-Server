import json

DASHBOARD_FILE = r"C:\tekla-mcp\dashboard.json"


def main():

    with open(
        DASHBOARD_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        dashboard = json.load(f)

    created = dashboard["created"]

    columns = int(created * 0.25)
    beams = int(created * 0.60)
    braces = created - columns - beams

    print()
    print("FABRICATION AGENT")
    print("=================")

    print(f"Columns : {columns}")
    print(f"Beams   : {beams}")
    print(f"Braces  : {braces}")

    report = {
        "columns": columns,
        "beams": beams,
        "braces": braces,
        "status": "FABRICATION_READY"
    }

    with open(
        r"C:\tekla-mcp\fabrication_report.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4
        )

    print()
    print("Fabrication Report Generated")


if __name__ == "__main__":

    main()