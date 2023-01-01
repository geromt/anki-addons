from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.operations import QueryOp
from aqt.qt import *

import subprocess
import os

from AutomaticBackup.utils import *


def autmatic_backup():
    config = mw.addonManager.getConfig(__name__)

    # If backup_dir doesn't exist, creates it
    if not os.path.exists(config["backup_dir"]):
        try:
            os.makedirs(config["backup_dir"])
        except PermissionError:
            showInfo("You don't have permissions to create backup_dir")
            return False

    # Remove the old backup file
    old_colpkg = find_colpkg_file(config["backup_dir"])
    if old_colpkg:
        subprocess.run(["rm", "-v", config["backup_dir"]+"/"+old_colpkg])

    if backup_collection(mw.col, config["backup_dir"], config["compress_colpkg"]):
        if config.get("include_media"):
            backup_media(config["backup_dir"], mw.pm.name, config["compress_media"])
        if config.get("upload_to_cloud"):
            copy_to_remote(config["backup_dir"], config["remote"])
        print("Backup successfully created")
        return True
    else:
        print("Failed to create backup file")
        return False


def on_success(state):
    if state:
        showInfo("Backup successfully created")
    else:
        showInfo("Failed to create backup file")


def ui_action():
    op = QueryOp(
        parent = mw,
        op = lambda col: autmatic_backup(),
        success = on_success
    )
    op.with_progress().run_in_background()

action = QAction("Automatic Backup", mw)
qconnect(action.triggered, ui_action)
mw.form.menuTools.addAction(action)
