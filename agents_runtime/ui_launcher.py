import tkinter as tk
import subprocess

ORCHESTRATOR = (
    r"C:\tekla-mcp\agents_runtime\orchestrator.py"
)


def run_workflow():

    subprocess.run(
        [
            "python",
            ORCHESTRATOR
        ]
    )


root = tk.Tk()

root.title("Steel AI Mind")

root.geometry("550x350")

title = tk.Label(
    root,
    text="STEEL AI MIND",
    font=("Arial", 20, "bold")
)

title.pack(pady=15)

tagline = tk.Label(
    root,
    text="Engineering Intelligence Platform",
    font=("Arial", 10)
)

tagline.pack()

status = tk.Label(
    root,
    text="STAAD → Tekla → Fabrication",
    font=("Arial", 11, "italic")
)

status.pack(pady=10)

run_button = tk.Button(
    root,
    text="Run Steel AI Mind Workflow",
    width=30,
    height=2,
    command=run_workflow
)

run_button.pack(pady=30)

root.mainloop()