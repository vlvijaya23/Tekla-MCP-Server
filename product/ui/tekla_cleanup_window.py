import tkinter as tk

from product.controllers.tekla_cleanup_controller import (
    detect_members,
    merge_members
)


class TeklaCleanupWindow:

    def __init__(self):

        self.window = tk.Toplevel()

        self.window.title(
            "Tekla Cleanup"
        )

        self.window.geometry(
            "450x450"
        )

        self.window.resizable(
            False,
            False
        )

        tk.Label(
            self.window,
            text="TEKLA CLEANUP",
            font=(
                "Arial",
                14,
                "bold",
                "underline"
            )
        ).pack(
            pady=10
        )

        button_frame = tk.Frame(
            self.window
        )

        button_frame.pack(
            pady=10
        )

        tk.Button(
            button_frame,
            text="Detect Members",
            width=18,
            height=2,
            command=self.detect_members
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Merge Members",
            width=18,
            height=2,
            command=self.merge_members
        ).pack(
            side="left",
            padx=5
        )

        output_frame = tk.Frame(
            self.window
        )

        output_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        scrollbar = tk.Scrollbar(
            output_frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.output = tk.Text(
            output_frame,
            height=8,
            yscrollcommand=scrollbar.set
        )

        self.output.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.output.yview
        )

        tk.Button(
            self.window,
            text="OK",
            width=12,
            command=self.window.destroy
        ).pack(
            pady=5
        )

    def detect_members(
        self
    ):

        result = (
            detect_members()
        )

        self.output.delete(
            "1.0",
            tk.END
        )

        if not result:

            self.output.insert(
                tk.END,
                "No split members found."
            )

            return

        self.output.insert(
            tk.END,
            f"Chains Found : {len(result)}\n\n"
        )

        for index, item in enumerate(
            result,
            start=1
        ):

            member_type = item.get(
                "type",
                ""
            )

            if (
                member_type
                == "COLUMN_CHAIN"
            ):

                self.output.insert(
                    tk.END,
                    (
                        f"CHAIN {index}\n"
                        f"Profile : {item['profile']}\n"
                        f"Seg : {item['segment_count']}\n"
                        f"Len : {item['length']} mm\n"
                        f"Sts : {item['status']}\n\n"
                    )
                )

                for member in item[
                    "members"
                ]:

                    self.output.insert(
                        tk.END,
                        f"{member}\n"
                    )

                self.output.insert(
                    tk.END,
                    "\n------------------\n\n"
                )

            elif (
                member_type
                == "BEAM_CHAIN"
            ):

                self.output.insert(
                    tk.END,
                    (
                        f"BEAM CHAIN {index}\n"
                        f"Profile : {item['profile']}\n"
                        f"Segments : {item['segment_count']}\n\n"
                    )
                )

                for member in item[
                    "members"
                ]:

                    self.output.insert(
                        tk.END,
                        f"{member}\n"
                    )

                self.output.insert(
                    tk.END,
                    "\n------------------\n\n"
                )

    def merge_members(
        self
    ):

        result = (
            merge_members()
        )

        self.output.delete(
            "1.0",
            tk.END
        )

        self.output.insert(
            tk.END,
            "MERGE RESULT\n\n"
        )

        self.output.insert(
            tk.END,
            str(result)
        )