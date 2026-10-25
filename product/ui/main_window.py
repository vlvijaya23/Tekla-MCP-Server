import tkinter as tk
import threading

from tkinter import ttk
from tkinter import filedialog

from product.ui.tekla_cleanup_window import (
    TeklaCleanupWindow
)

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

from product.version import (
    APP_VERSION
)

from product.analytics import (
    log_event
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
            f"Tekla AI Modeler v{APP_VERSION}"
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
            text=f"TEKLA AI MODELER v{APP_VERSION}",
            font=(
                "Arial",
                18,
                "bold",
                "underline"
            )
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
            width=18,
            height=1,
            font=(
                "Arial",
                10,
            ),
            command=self.analyze_model
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Create Tekla Model",
            width=18,
            height=1,
            font=(
                "Arial",
                10,
            ),
            command=self.create_model
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Tekla Cleanup",
            width=18,
            height=1,
            font=(
                "Arial",
                10,
            ),
            command=self.open_cleanup_window
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="OK",
            width=12,
            height=1,
            font=(
                "Arial",
                10,
            ),
            command=self.root.destroy
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

        log_event(
            "ANALYZE_MODEL"
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

    def create_model(
        self
    ):

        file_path = (
            self.staad_file.get()
        )

        if not file_path:

            self.status.set(
                "Please select STAAD file"
            )

            return

        self.progress_window = (
            tk.Toplevel(
                self.root
            )
        )

        self.progress_window.title(
            "Processing"
        )

        self.progress_window.geometry(
            "350x120"
        )

        self.progress_window.resizable(
            False,
            False
        )

        self.progress_window.transient(
            self.root
        )

        self.progress_window.grab_set()

        tk.Label(
            self.progress_window,
            text=(
                "Creating Tekla Model...\n\n"
                "Please wait."
            ),
            font=(
                "Arial",
                10,
                "bold"
            )
        ).pack(
            pady=10
        )

        self.progress = (
            ttk.Progressbar(
                self.progress_window,
                mode="determinate",
                length=250,
                maximum=100
            )
        )

        self.progress.pack(
            pady=10
        )

        self.progress_label = tk.Label(
            self.progress_window,
            text="0%"
        )

        self.progress_label.pack(
            pady=5
        )

        self.progress["value"] = 0

        self.status.set(
            "Creating Tekla Model..."
        )

        threading.Thread(
            target=self.run_import,
            args=(file_path,),
            daemon=True
        ).start()

    def run_import(
        self,
        file_path
    ):

        try:

            log_event(
                "CREATE_MODEL"
            )

            result = (
                self.tekla_import_controller
                .create_model(
                    file_path,
                    self.update_progress
                )
            )

            self.root.after(
                0,
                lambda:
                self.import_completed(
                    result
                )
            )

        except Exception as ex:

            self.root.after(
                0,
                lambda:
                self.import_failed(
                    str(ex)
                )
            )

    def open_cleanup_window(
        self
    ):

        TeklaCleanupWindow()

    def import_completed(
        self,
        result
    ):

        tekla = result[
            "tekla"
        ]

        self.status.set(
            f"Created {tekla['created']} | "
            f"Failed {tekla['failed']} | "
            f"Skipped {tekla['skipped']}"
        )

        self.progress.configure(
            value=100
        )

        self.progress_label.config(
            text="100%"
        )

        self.progress_window.destroy()

        ImportReportWindow(
            result
        )

    def import_failed(
        self,
        error
    ):

        self.progress.configure(
            value=0
        )

        self.progress_window.destroy()

        self.status.set(
            f"Error : {error}"
        )

    def update_progress(
        self,
        value
    ):

        self.root.after(
            0,
            lambda:
            self.progress.configure(
                value=value
            )
        )

        self.root.after(
            0,
            lambda:
            self.progress_label.config(
                text=f"{value}%"
            )
        )