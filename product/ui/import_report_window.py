import json
import os
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
            f"900x{700}"
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

        report_file = (
            r"C:\tekla-mcp\root_cause_report.json"
        )

        if os.path.exists(
            report_file
        ):

            root_frame = tk.LabelFrame(
                window,
                text="ROOT CAUSE SUMMARY"
            )

            root_frame.pack(
                fill="x",
                padx=10,
                pady=5
            )

            with open(
                report_file,
                "r",
                encoding="utf-8"
            ) as f:

                report = json.load(
                    f
                )

            for profile, count in sorted(
                report.items(),
                key=lambda x: x[1],
                reverse=True
            ):

                tk.Label(
                    root_frame,
                    text=(
                        f"{profile} : "
                        f"{count} failure(s)"
                    )
                ).pack(
                    anchor="w"
                )

        tree_frame = tk.LabelFrame(
            window,
            text=(
                f"FAILURE INTELLIGENCE "
                f"({tekla['failed']} Failed)"
            )
        )

        tree_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        failure_container = tk.Frame(
            tree_frame
        )

        failure_container.pack(
            fill="both",
            expand=True
        )

        failure_scrollbar = ttk.Scrollbar(
            failure_container,
            orient="vertical"
        )

        failure_scrollbar.pack(
            side="right",
            fill="y"
        )

        tree = ttk.Treeview(
            failure_container,
            columns=(
                "member",
                "profile",
                "reason"
            ),
            show="headings",
            yscrollcommand=(
                failure_scrollbar.set
            )
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
            side="left",
            fill="both",
            expand=True
        )

        failure_scrollbar.config(
            command=tree.yview
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

        skipped_frame = tk.LabelFrame(
            window,
            text=(
                f"SKIPPED MEMBER INTELLIGENCE "
                f"({tekla['skipped']} Skipped)"
            )
        )

        skipped_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        skipped_container = tk.Frame(
            skipped_frame
        )

        skipped_container.pack(
            fill="both",
            expand=True
        )

        skipped_scrollbar = ttk.Scrollbar(
            skipped_container,
            orient="vertical"
        )

        skipped_scrollbar.pack(
            side="right",
            fill="y"
        )

        skipped_tree = ttk.Treeview(
            skipped_container,
            columns=(
                "member",
                "profile",
                "reason",
                "length"
            ),
            show="headings",
            yscrollcommand=(
                skipped_scrollbar.set
            )
        )

        skipped_tree.heading(
            "member",
            text="MEMBER"
        )

        skipped_tree.heading(
            "profile",
            text="PROFILE"
        )

        skipped_tree.heading(
            "reason",
            text="REASON"
        )

        skipped_tree.heading(
            "length",
            text="LENGTH"
        )

        skipped_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        skipped_scrollbar.config(
            command=skipped_tree.yview
        )

        for skipped in tekla.get(
            "skipped_members",
            []
        ):

            skipped_tree.insert(
                "",
                "end",
                values=(
                    skipped.get(
                        "member",
                        ""
                    ),
                    skipped.get(
                        "profile",
                        ""
                    ),
                    skipped.get(
                        "reason",
                        ""
                    ),
                    round(
                        float(
                            skipped.get(
                                "length",
                                0
                            )
                        ),
                        3
                    )
                )
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
            width=15,
            height=1,
            command=window.destroy
        ).pack(
            side="left",
            padx=10
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
