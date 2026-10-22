import tkinter as tk
import json
import os
from tkinter import messagebox
from datetime import datetime
import uuid
import base64
import subprocess

from product.updater import (
    check_for_updates,
    copy_update_installer
)

from product.version import (
    APP_VERSION
)

from product.analytics import (
    log_event
)

from product.ui.main_window import MainWindow

def get_machine_id():

    return str(
        uuid.getnode()
    )

def validate_license():

    license_file = (
        r"C:\tekla-mcp\license.key"
    )

    if not os.path.exists(
        license_file
    ):

        messagebox.showerror(
            "License Error",
            (
                "License file not found\n\n"
                f"Machine ID:\n"
                f"{get_machine_id()}\n\n"
                "Send this Machine ID "
                "to Administrator."
            )
        )

        return False

    with open(
        license_file,
        "r",
        encoding="utf-8"
    ) as f:

        encoded = (
            f.read()
            .strip()
        )

    decoded = (
        base64.b64decode(
            encoded
        ).decode()
    )

    license_data = json.loads(
        decoded
    )

    if not license_data.get(
        "enabled",
        False
    ):

        messagebox.showerror(
            "License Error",
            "License disabled"
        )

        return False

    expiry = datetime.strptime(
        license_data["expiry"],
        "%Y-%m-%d"
    )

    if datetime.now() > expiry:

        messagebox.showerror(
            "License Error",
            (
                "License expired\n\n"
                f"Machine ID:\n"
                f"{get_machine_id()}"
            )
        )

        return False

    current_machine = (
        get_machine_id()
    )

    licensed_machines = (
        license_data.get(
            "machine_ids",
            []
        )
    )

    if (
        current_machine
        not in licensed_machines
    ):

        messagebox.showerror(
            "License Error",
            (
                "Machine not authorized\n\n"
                f"Machine ID:\n"
                f"{current_machine}\n\n"
                "Send this Machine ID "
                "to Administrator."
            )
        )

        return False

    return True

def main():

    if not validate_license():

        return

    latest = (
        check_for_updates()
    )

    if latest:

        update_now = (
            messagebox.askyesno(
                "Update Available",
                (
                    f"Current Version: "
                    f"{APP_VERSION}\n\n"
                    f"Latest Version: "
                    f"{latest}\n\n"
                    "Install update now?"
                )
            )
        )

        if update_now:

            installer = (
                copy_update_installer()
            )

            if installer:

                subprocess.Popen(
                    installer
                )

                return

    log_event(
        "APPLICATION_STARTED"
    )

    root = tk.Tk()

    MainWindow(root)

    root.mainloop()

if __name__ == "__main__":
    main()