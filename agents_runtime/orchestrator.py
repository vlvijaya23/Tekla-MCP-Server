import subprocess
import os

BASE_DIR = r"C:\tekla-mcp\agents_runtime"

GEOMETRY_AGENT = os.path.join(
    BASE_DIR,
    "geometry_agent.py"
)

PROFILE_AGENT = os.path.join(
    BASE_DIR,
    "profile_agent.py"
)


def run_agent(name, path):

    print()
    print("=" * 50)
    print(f"RUNNING {name}")
    print("=" * 50)

    subprocess.run(
        ["python", path],
        check=False
    )


def main():

    print()
    print("TEKLA MCP ORCHESTRATOR")
    print("=" * 50)

    run_agent(
        "GEOMETRY AGENT",
        GEOMETRY_AGENT
    )

    run_agent(
        "PROFILE AGENT",
        PROFILE_AGENT
    )

    print()
    print("=" * 50)
    print("WORKFLOW COMPLETE")
    print("=" * 50)


if __name__ == "__main__":

    main()