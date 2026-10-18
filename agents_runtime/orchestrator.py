import subprocess
import os

BASE_DIR = r"C:\tekla-mcp\agents_runtime"

AGENTS = [
    ("CLASSIFICATION AGENT", "classification_agent.py"),
    ("NAMING AGENT", "naming_agent.py"),
    ("POSITION AGENT", "position_agent.py"),
    ("QUALITY AGENT", "quality_agent.py"),
    ("GEOMETRY AGENT", "geometry_agent.py"),
    ("PROFILE AGENT", "profile_agent.py"),
    ("DASHBOARD AGENT", "dashboard_agent.py"),
    ("FABRICATION AGENT", "fabrication_agent.py")
]


def run_agent(title, script):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

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
    print("STEEL AI MIND")
    print("ENGINEERING INTELLIGENCE PIPELINE")
    print("=" * 60)

    for title, script in AGENTS:

        run_agent(
            title,
            script
        )

    print()
    print("=" * 60)
    print("STEEL AI MIND COMPLETE")
    print("=" * 60)


if __name__ == "__main__":

    main()