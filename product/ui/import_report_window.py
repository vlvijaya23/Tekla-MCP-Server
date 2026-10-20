import tkinter as tk
from tkinter import ttk


class ImportReportWindow:

    def __init__(
        self,
        result
    ):

        window = tk.Toplevel()

        window.title(
            "AI Import Report"
        )

        error_count = len(
            result["tekla"].get(
                "errors",
                []
            )
        )

        height = max(
            350,
            min(
                650,
                250 + (
                    error_count * 30
                )
            )
        )

        window.geometry(
            f"900x{height}"
        )

        window.resizable(
            False,
            False
        )

        window.transient()

        window.grab_set()

        summary = tk.LabelFrame(
            window,
            text="IMPORT SUMMARY"
        )

        summary.pack(
            fill="x",
            padx=10,
            pady=10
        )

        tekla = result["tekla"]

        tk.Label(
            summary,
            text=f"Created : {tekla['created']}"
        ).pack(anchor="w")

        tk.Label(
            summary,
            text=f"Failed : {tekla['failed']}"
        ).pack(anchor="w")

        tk.Label(
            summary,
            text=f"Skipped : {tekla['skipped']}"
        ).pack(anchor="w")

        tree_frame = tk.LabelFrame(
            window,
            text="FAILURE INTELLIGENCE"
        )

        tree_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        tree = ttk.Treeview(
            tree_frame,
            columns=(
                "member",
                "profile",
                "reason"
            ),
            show="headings"
        )

        tree.heading(
            "member",
            text="MEMBER"
        )

        tree.heading(
            "profile",
            text="PROFILE"
        )

        tree.heading(
            "reason",
            text="AI DIAGNOSIS"
        )

        tree.pack(
            fill="x",
            expand=False
        )

        for error in tekla.get(
            "errors",
            []
        ):

            member = error.get(
                "member",
                "UNKNOWN"
            )

            profile = error.get(
                "profile",
                "UNKNOWN"
            )

            reason = (
                self.diagnose(
                    error
                )
            )

            tree.insert(
                "",
                "end",
                values=(
                    member,
                    profile,
                    reason
                )
            )

        tk.Button(
            window,
            text="OK",
            width=15,
            command=window.destroy
        ).pack(
            pady=10
        )

    def diagnose(
        self,
        error
    ):

        text = str(
            error
        ).upper()

        if "SHORT_MEMBER" in text:

            return (
                "Member too short for Tekla"
            )

        if "PROFILE" in text:

            return (
                "Profile mapping issue"
            )

        if "INSERT" in text:

            return (
                "Tekla insert failed"
            )

        return (
            "Review required"
        )

        button_frame = tk.Frame(
            window
        )

        button_frame.pack(
            fill="x",
            pady=10
        )

        tk.Button(
            button_frame,
            text="OK",
            width=20,
            height=2,
            command=window.destroy
        ).pack(
            pady=5
        )