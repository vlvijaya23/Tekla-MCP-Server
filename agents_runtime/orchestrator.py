import subprocess
import os

BASE_DIR = r"C:\tekla-mcp\agents_runtime"

AGENTS = [
    ("GEOMETRY AGENT", "geometry_agent.py"),
    ("PROFILE AGENT", "profile_agent.py"),
    ("DASHBOARD AGENT", "dashboard_agent.py"),
    ("FABRICATION AGENT", "fabrication_agent.py")
]


def run_agent(title, script):

    print()
    print("=" * 50)
    print(title)
    print("=" * 50)

    subprocess.run(
        [
            "python",
            os.path.join(
                BASE_DIR,
                script
            )
        ]
    )


def main():

    print()
    print("TEKLA MCP ORCHESTRATOR")
    print("=" * 50)

    for title, script in AGENTS:

        run_agent(
            title,
            script
        )

    print()
    print("=" * 50)
    print("MCP WORKFLOW COMPLETE")
    print("=" * 50)


if __name__ == "__main__":

    main()