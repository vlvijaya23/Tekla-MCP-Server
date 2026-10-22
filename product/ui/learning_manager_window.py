import tkinter as tk

from product.controllers.profile_learning_engine import (
    ProfileLearningEngine
)


class LearningManagerWindow:

    def __init__(
        self,
        profiles,
        refresh_callback=None
    ):

        self.engine = (
            ProfileLearningEngine()
        )

        self.profiles = (
            profiles
        )

        self.refresh_callback = (
            refresh_callback
        )

        self.index = 0

        self.window = tk.Toplevel()

        self.window.title(
            "AI Learning Manager"
        )

        self.window.geometry(
            "700x300"
        )

        self.window.resizable(
            False,
            False
        )

        self.header_label = tk.Label(
            self.window,
            font=(
                "Arial",
                12,
                "bold"
            )
        )

        self.header_label.pack(
            pady=10
        )

        self.profile_label = tk.Label(
            self.window,
            font=(
                "Arial",
                10
            )
        )

        self.profile_label.pack(
            pady=10
        )

        tk.Label(
            self.window,
            text="Tekla Profile"
        ).pack(
            pady=5
        )

        self.tekla_profile = (
            tk.StringVar()
        )

        tk.Entry(
            self.window,
            textvariable=self.tekla_profile,
            width=50
        ).pack(
            pady=5
        )

        button_frame = tk.Frame(
            self.window
        )

        button_frame.pack(
            pady=15
        )

        self.learn_button = tk.Button(
            button_frame,
            text="Learn & Next",
            width=20,
            command=self.learn
        )

        self.learn_button.pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Skip",
            width=20,
            command=self.next_profile
        ).pack(
            side="left",
            padx=5
        )

        self.load_profile()

    def load_profile(
        self
    ):

        current = (
            self.profiles[
                self.index
            ]
        )

        self.header_label.config(
            text=(
                f"Unknown Profile "
                f"{self.index + 1}"
                f" of "
                f"{len(self.profiles)}"
            )
        )

        self.profile_label.config(
            text=current
        )

        self.tekla_profile.set(
            ""
        )

        if (
            self.index
            ==
            len(
                self.profiles
            ) - 1
        ):

            self.learn_button.config(
                text="Learn & Finish"
            )

    def learn(
        self
    ):

        value = (
            self.tekla_profile.get()
            .strip()
        )

        if not value:

            return

        current = (
            self.profiles[
                self.index
            ]
        )

        self.engine.save_mapping(
            current,
            value
        )

        self.next_profile()

    def next_profile(
        self
    ):

        self.index += 1

        if (
            self.index
            >=
            len(
                self.profiles
            )
        ):

            self.window.destroy()

            if (
                self.refresh_callback
            ):

                self.refresh_callback()

            return

        self.load_profile()