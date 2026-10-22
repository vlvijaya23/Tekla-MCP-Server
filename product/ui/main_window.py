import tkinter as tk
from tkinter import filedialog

from product.ui.import_report_window import (
    ImportReportWindow
)

from product.controllers.analysis_controller import (
    AnalysisController
)

from product.controllers.profile_intelligence import (
    ProfileIntelligence
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

        self.last_result = None

        root.title(
            "Tekla AI Modeler"
        )

        root.geometry(
            "600x300"
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
            font=("Arial", 18, "bold", "underline")
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

        self.last_result = result

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

    def ask_copilot(
        self
    ):

        question = (
            self.copilot_question.get()
            .strip()
            .lower()
        )

        if not question:

            return

        if not self.last_result:

            self.status.set(
                "Analyze a model first"
            )

            return

        result = self.last_result

        if (
            "unmapped" in question
            or
            "review" in question
            or
            "learning" in question
            or
            "need learning" in question
            or
            "profiles needing learning" in question
            or
            "review required" in question
        ):

            intelligence = (
                ProfileIntelligence()
            )

            unmapped = []

            for profile in result.get(
                "profiles",
                []
            ):

                mapping = (
                    intelligence.infer_mapping(
                        profile
                    )
                )

                if (
                    mapping["tekla"]
                    == "REVIEW_REQUIRED"
                ):

                    unmapped.append(
                        profile
                    )

            if unmapped:

                self.status.set(
                    f"Unmapped Profiles : {len(unmapped)}"
                )

                popup = tk.Toplevel()

                popup.title(
                    "Copilot Result"
                )

                popup.geometry(
                    "700x300"
                )

                text = tk.Text(
                    popup
                )

                text.pack(
                    fill="both",
                    expand=True
                )

                for profile in unmapped:

                    text.insert(
                        tk.END,
                        f"{profile}\n"
                    )

            else:

                self.status.set(
                    "No unmapped profiles found"
                )

        elif (
            "member" in question
        ):

            self.status.set(
                f"Members : {result['members']}"
            )

        elif (
            "profile" in question
        ):

            self.status.set(
                f"Profiles : {len(result['profiles'])}"
            )

        elif (
            "column" in question
        ):

            self.status.set(
                f"Columns : {result['columns']}"
            )

        elif (
            "beam" in question
        ):

            self.status.set(
                f"Beams : {result['beams']}"
            )

        elif (
            "brace" in question
        ):

            self.status.set(
                f"Braces : {result['braces']}"
            )

        elif (
            "node" in question
        ):

            self.status.set(
                f"Nodes : {result['nodes']}"
            )

        elif (
            "group" in question
        ):

            self.status.set(
                f"Groups : {result['groups']}"
            )

        else:

            self.status.set(
                "Question not understood"
            )