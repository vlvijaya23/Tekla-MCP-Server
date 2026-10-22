import json
import os
import shutil

from product.version import (
    APP_VERSION
)


UPDATE_FOLDER = (
    r"\\SERVER\TeklaAIModeler"
)


def check_for_updates():

    version_file = os.path.join(
        UPDATE_FOLDER,
        "version.json"
    )

    if not os.path.exists(
        version_file
    ):

        return None

    with open(
        version_file,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(
            f
        )

    latest = data.get(
        "version",
        APP_VERSION
    )

    if latest != APP_VERSION:

        return latest

    return None


def get_installer_path():

    installer = os.path.join(
        UPDATE_FOLDER,
        "TeklaAIModelerSetup.exe"
    )

    if os.path.exists(
        installer
    ):

        return installer

    return None

def copy_update_installer():

    installer = (
        get_installer_path()
    )

    if not installer:

        return None

    local_installer = (
        r"C:\Temp\TeklaAIModelerSetup.exe"
    )

    os.makedirs(
        r"C:\Temp",
        exist_ok=True
    )

    shutil.copy2(
        installer,
        local_installer
    )

    return local_installer

