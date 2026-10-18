import tkinter as tk
import subprocess
import json
import os

ORCHESTRATOR = (
    r"C:\tekla-mcp\agents_runtime\orchestrator.py"
)

DASHBOARD = (
    r"C:\tekla-mcp\dashboard.json"
)


def load_dashboard():

    if not os.path.exists(
        DASHBOARD
    ):

        return {
            "created": 0,
            "failed": 0,
            "skipped": 0,
            "recovery_rate": 0
        }

    with open(
        DASHBOARD,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def refresh_dashboard():

    data = load_dashboard()

    imported_var.set(
        str(
            data.get(
                "created",
                0
            )
        )
    )

    failed_var.set(
        str(
            data.get(
                "failed",
                0
            )
        )
    )

    skipped_var.set(
        str(
            data.get(
                "skipped",
                0
            )
        )
    )

    recovery_var.set(
        f'{data.get("recovery_rate", 0)}%'
    )


def run_workflow():

    subprocess.run(
        [
            "python",
            ORCHESTRATOR
        ]
    )

    refresh_dashboard()


def open_dashboard():

    os.startfile(
        r"C:\tekla-mcp\dashboard.json"
    )


def open_failed_members():

    os.startfile(
        r"C:\tekla-mcp\failed_members.json"
    )


def open_project_folder():

    os.startfile(
        r"C:\tekla-mcp"
    )


root = tk.Tk()

root.title(
    "Steel AI Mind"
)

root.geometry(
    "700x650"
)

root.resizable(
    False,
    False
)

title = tk.Label(
    root,
    text="STEEL AI MIND",
    font=(
        "Arial",
        24,
        "bold"
    )
)

title.pack(
    pady=10
)

tagline = tk.Label(
    root,
    text="Engineering Intelligence Platform",
    font=(
        "Arial",
        11
    )
)

tagline.pack()

flow = tk.Label(
    root,
    text="STAAD → Tekla → Fabrication",
    font=(
        "Arial",
        10,
        "italic"
    )
)

flow.pack(
    pady=5
)

frame = tk.LabelFrame(
    root,
    text="IMPORT STATUS",
    padx=10,
    pady=10
)

frame.pack(
    pady=15,
    padx=20,
    fill="x"
)

imported_var = tk.StringVar()

failed_var = tk.StringVar()

skipped_var = tk.StringVar()

recovery_var = tk.StringVar()

tk.Label(
    frame,
    text="Imported :",
    width=15,
    anchor="w"
).grid(
    row=0,
    column=0
)

tk.Label(
    frame,
    textvariable=imported_var
).grid(
    row=0,
    column=1
)

tk.Label(
    frame,
    text="Failed :",
    width=15,
    anchor="w"
).grid(
    row=1,
    column=0
)

tk.Label(
    frame,
    textvariable=failed_var
).grid(
    row=1,
    column=1
)

tk.Label(
    frame,
    text="Skipped :",
    width=15,
    anchor="w"
).grid(
    row=2,
    column=0
)

tk.Label(
    frame,
    textvariable=skipped_var
).grid(
    row=2,
    column=1
)

tk.Label(
    frame,
    text="Recovery :",
    width=15,
    anchor="w"
).grid(
    row=3,
    column=0
)

tk.Label(
    frame,
    textvariable=recovery_var
).grid(
    row=3,
    column=1
)

button_frame = tk.Frame(
    root
)

button_frame.pack(
    pady=15
)

run_button = tk.Button(
    button_frame,
    text="Run Steel AI Mind Workflow",
    width=30,
    height=2,
    command=run_workflow
)

run_button.pack(
    pady=5
)

refresh_button = tk.Button(
    button_frame,
    text="Refresh Dashboard",
    width=30,
    command=refresh_dashboard
)

refresh_button.pack(
    pady=5
)

dashboard_button = tk.Button(
    button_frame,
    text="Open Dashboard",
    width=30,
    command=open_dashboard
)

dashboard_button.pack(
    pady=5
)

failed_button = tk.Button(
    button_frame,
    text="Open Failed Members",
    width=30,
    command=open_failed_members
)

failed_button.pack(
    pady=5
)

folder_button = tk.Button(
    button_frame,
    text="Open Project Folder",
    width=30,
    command=open_project_folder
)

folder_button.pack(
    pady=5
)

refresh_dashboard()

root.mainloop()