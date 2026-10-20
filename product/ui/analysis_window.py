import tkinter as tk
from tkinter import ttk

from product.controllers.profile_intelligence import (
    ProfileIntelligence
)

from product.controllers.approval_engine import (
    ApprovalEngine
)


class AnalysisWindow:

    def __init__(self, result):

        window = tk.Toplevel()

        window.title(
            "Analysis Dashboard"
        )

        window.geometry(
            "900x680"
        )

        window.resizable(
            False,
            False
        )

        summary_frame = tk.LabelFrame(
            window,
            text="PROJECT SUMMARY"
        )

        summary_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        tk.Label(
            summary_frame,
            text=f"Members Found : {result.get('members', 0)}"
        ).pack(anchor="w")

        tk.Label(
            summary_frame,
            text=f"Profiles Found : {len(result.get('profiles', []))}"
        ).pack(anchor="w")

        tk.Label(
            summary_frame,
            text=f"Mapped Profiles : {result.get('mapped_profiles', 0)}"
        ).pack(anchor="w")

        tk.Label(
            summary_frame,
            text=f"Columns : {result.get('columns', 0)}"
        ).pack(anchor="w")

        tk.Label(
            summary_frame,
            text=f"Beams : {result.get('beams', 0)}"
        ).pack(anchor="w")

        tk.Label(
            summary_frame,
            text=f"Braces : {result.get('braces', 0)}"
        ).pack(anchor="w")

        mapping_frame = tk.LabelFrame(
            window,
            text="AI PROFILE MAPPING"
        )

        mapping_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        tree = ttk.Treeview(
            mapping_frame,
            columns=(
                "staad",
                "tekla",
                "confidence",
                "status"
            ),
            show="headings"
        )

        tree.heading(
            "staad",
            text="STAAD PROFILE"
        )

        tree.heading(
            "tekla",
            text="TEKLA PROFILE"
        )

        tree.heading(
            "confidence",
            text="CONFIDENCE"
        )

        tree.heading(
            "status",
            text="STATUS"
        )

        tree.column(
            "staad",
            width=250
        )

        tree.column(
            "tekla",
            width=250
        )

        tree.column(
            "confidence",
            width=100
        )

        tree.column(
            "status",
            width=150
        )

        tree.pack(
            fill="both",
            expand=True
        )

        intelligence = (
            ProfileIntelligence()
        )

        approval = (
            ApprovalEngine()
        )

        auto_approved = 0
        review_required = 0

        for profile in sorted(
            result.get(
                "profiles",
                []
            )
        ):

            ai_result = (
                intelligence.infer_mapping(
                    profile
                )
            )

            status, color = (
                approval.evaluate(
                    ai_result["confidence"]
                )
            )

            if status == "AUTO APPROVED":

                auto_approved += 1

            else:

                review_required += 1

            tree.insert(
                "",
                "end",
                values=(
                    profile,
                    ai_result["tekla"],
                    f"{ai_result['confidence']}%",
                    status
                )
            )

        decision_frame = tk.LabelFrame(
            window,
            text="AI DECISION SUMMARY"
        )

        decision_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        tk.Label(
            decision_frame,
            text=f"Auto Approved : {auto_approved}"
        ).pack(anchor="w")

        tk.Label(
            decision_frame,
            text=f"Review Required : {review_required}"
        ).pack(anchor="w")

        log_frame = tk.LabelFrame(
            window,
            text="ANALYSIS LOG"
        )

        log_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        log_box = tk.Text(
            log_frame,
            height=3
        )

        log_box.pack(
            fill="x"
        )

        log_box.insert(
            tk.END,
            "STAAD File Loaded\n"
        )

        log_box.insert(
            tk.END,
            f"Profiles Detected : {len(result.get('profiles', []))}\n"
        )

        log_box.insert(
            tk.END,
            f"Members Detected : {result.get('members', 0)}\n"
        )

        log_box.insert(
            tk.END,
            "AI Profile Analysis Complete\n"
        )

        log_box.config(
            state="disabled"
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
