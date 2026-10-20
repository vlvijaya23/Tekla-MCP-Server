import tkinter as tk
from tkinter import filedialog

from product.ui.import_report_window import (
    ImportReportWindow
)

from product.controllers.analysis_controller import (
    AnalysisController
)

from product.ui.analysis_window import (
    AnalysisWindow
)

from product.controllers.tekla_import_controller import (
    TeklaImportController
)

class MainWindow:

    def __init__(self, root):

        self.root = root

        self.tekla_import_controller = (
            TeklaImportController()
        )

        self.analysis_controller = (
            AnalysisController()
        )

        root.title(
            "Tekla AI Modeler"
        )

        root.geometry(
            "700x800"
        )
        root.resizable(
            False,
            False
        )

        #
        # Title
        #

        title = tk.Label(
            root,
            text="TEKLA AI MODELER",
            font=("Arial", 18, "bold")
        )

        title.pack(
            pady=15
        )

        #
        # STAAD FILE
        #

        self.staad_file = tk.StringVar()

        file_frame = tk.LabelFrame(
            root,
            text="STAAD FILE",
            padx=10,
            pady=10
        )

        file_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        file_inner = tk.Frame(
            file_frame
        )

        file_inner.pack(
            fill="x"
        )

        tk.Entry(
            file_inner,
            textvariable=self.staad_file
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        tk.Button(
            file_inner,
            text="Browse",
            width=10,
            command=self.browse_staad
        ).pack(
            side="right"
        )

        #
        # Analysis Variables
        #

        self.profile_count = tk.StringVar(
            value="0"
        )

        self.member_count = tk.StringVar(
            value="0"
        )

        self.column_count = tk.StringVar(
            value="0"
        )

        self.beam_count = tk.StringVar(
            value="0"
        )

        self.brace_count = tk.StringVar(
            value="0"
        )

        self.mapped_count = tk.StringVar(
            value="0"
        )

        #
        # ANALYSIS PANEL
        #

        analysis_frame = tk.LabelFrame(
            root,
            text="ANALYSIS RESULTS",
            padx=10,
            pady=10
        )

        analysis_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            analysis_frame,
            text="Profiles Found:"
        ).grid(row=0, column=0, sticky="w", padx=5)

        tk.Label(
            analysis_frame,
            textvariable=self.profile_count,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=1, sticky="w")

        tk.Label(
            analysis_frame,
            text="Columns:"
        ).grid(row=0, column=2, sticky="w", padx=20)

        tk.Label(
            analysis_frame,
            textvariable=self.column_count,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=3, sticky="w")

        tk.Label(
            analysis_frame,
            text="Beams:"
        ).grid(row=0, column=4, sticky="w", padx=20)

        tk.Label(
            analysis_frame,
            textvariable=self.beam_count,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=5, sticky="w")

        tk.Label(
            analysis_frame,
            text="Braces:"
        ).grid(row=0, column=6, sticky="w", padx=20)

        tk.Label(
            analysis_frame,
            textvariable=self.brace_count,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=7, sticky="w")

        #
        # PROFILE MAPPING PANEL
        #

        profile_frame = tk.LabelFrame(
            root,
            text="PROFILE MAPPING",
            padx=10,
            pady=10
        )

        profile_frame.pack(
            fill="both",
            padx=20,
            pady=10
        )

        self.profile_list = tk.Text(
            profile_frame,
            height=3
        )

        self.profile_list.pack(
            fill="both",
            expand=True
        )

        #
        # OPTIONS
        #

        options_frame = tk.LabelFrame(
            root,
            text="OPTIONS",
            padx=10,
            pady=10
        )

        options_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.auto_mapping = tk.BooleanVar(
            value=True
        )

        self.auto_classification = tk.BooleanVar(
            value=True
        )

        self.auto_merge = tk.BooleanVar(
            value=True
        )

        self.qa_validation = tk.BooleanVar(
            value=True
        )

        tk.Checkbutton(
            options_frame,
            text="Auto Profile Mapping",
            variable=self.auto_mapping
        ).pack(anchor="w")

        tk.Checkbutton(
            options_frame,
            text="Auto Classification",
            variable=self.auto_classification
        ).pack(anchor="w")

        tk.Checkbutton(
            options_frame,
            text="Auto Column Merge",
            variable=self.auto_merge
        ).pack(anchor="w")

        tk.Checkbutton(
            options_frame,
            text="QA Validation",
            variable=self.qa_validation
        ).pack(anchor="w")

        #
        # PROJECT SUMMARY
        #

        summary_frame = tk.LabelFrame(
            root,
            text="PROJECT SUMMARY",
            padx=10,
            pady=10
        )

        summary_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            summary_frame,
            text="Members Found:"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        tk.Label(
            summary_frame,
            textvariable=self.member_count,
            font=("Arial", 10, "bold")
        ).grid(
            row=0,
            column=1,
            sticky="w"
        )

        #
        # COPILOT
        #

        copilot_frame = tk.LabelFrame(
            root,
            text="COPILOT",
            padx=10,
            pady=10
        )

        copilot_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.copilot_question = tk.StringVar()

        copilot_inner = tk.Frame(
            copilot_frame
        )

        copilot_inner.pack(
            fill="x"
        )

        tk.Entry(
            copilot_inner,
            textvariable=self.copilot_question
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        tk.Button(
            copilot_inner,
            text="Send",
            width=10,
            command=self.ask_copilot
        ).pack(
            side="right"
        )

        #
        # STATUS
        #

        self.status = tk.StringVar(
            value="Ready"
        )

        status_frame = tk.LabelFrame(
            root,
            text="STATUS"
        )

        status_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            status_frame,
            textvariable=self.status
        ).pack(
            anchor="w",
            padx=10,
            pady=5
        )

        #
        # BUTTONS
        #

        button_frame = tk.Frame(
            root
        )

        button_frame.pack(
            pady=10
        )

        tk.Button(
            button_frame,
            text="Analyze Model",
            width=25,
            height=3,
            font=(
                "Arial",
                10,
                "bold"
            ),
            command=self.analyze_model
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Create Tekla Model",
            width=25,
            height=3,
            font=(
                "Arial",
                10,
                "bold"
            ),
            command=self.create_model
        ).pack(
            side="left",
            padx=5
        )

    def browse_staad(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("STAAD Files", "*.std")
            ]
        )

        if file_path:

            self.staad_file.set(
                file_path
            )

            self.status.set(
                "STAAD file selected"
            )

    def analyze_model(self):

        file_path = self.staad_file.get()

        if not file_path:

            self.status.set(
                "Please select STAAD file"
            )

            return

        self.status.set(
            "Analyzing STAAD model..."
        )

        result = (
            self.analysis_controller
            .analyze_staad(
                file_path
            )
        )

        self.profile_list.delete(
            1.0,
            tk.END
        )

        for profile in result["profiles"]:

            self.profile_list.insert(
                tk.END,
                f"{profile}\n"
            )

        self.member_count.set(
            str(
                result["members"]
            )
        )

        self.column_count.set(
            str(
                result["columns"]
            )
        )

        self.beam_count.set(
            str(
                result["beams"]
            )
        )

        self.brace_count.set(
            str(
                result["braces"]
            )
        )

        self.profile_count.set(
            str(
                len(
                    result["profiles"]
                )
            )
        )

        self.status.set(
            "Analysis Complete"
        )

        AnalysisWindow(
            result
        )

    def create_model(self):

        file_path = self.staad_file.get()

        if not file_path:

            self.status.set(
                "Please select STAAD file"
            )

            return

        try:

            result = (
                self.tekla_import_controller
                .create_model(
                    file_path
                )
            )

            tekla = result["tekla"]

            self.status.set(
                f"Created {tekla['created']} | "
                f"Failed {tekla['failed']} | "
                f"Skipped {tekla['skipped']}"
            )

            ImportReportWindow(
                result
            )

        except Exception as ex:

            self.status.set(
                f"Error : {str(ex)}"
            )

    def ask_copilot(self):

        question = (
            self.copilot_question.get()
        )

        if not question:

            return

        self.status.set(
            f"Copilot received: {question}"
        )

    def ask_copilot(self):

        question = (
            self.copilot_question.get()
        )

        if not question:

            return

        self.status.set(
            f"Copilot received: {question}"
        )