"""Collection of functions for AutomaticBackup add-on"""

import subprocess
import os
import re

def backup_collection(col, backup_folder: str, compress_colpkg: bool) -> bool:
    """Create the backup file of the collection

    :param backup_folder: Path of the directory where backup file will be saved.
    :param compress_colpkg: Indicates if the backup file must be compressed. If
        True, it use gzip command line tool to compress the file.
    :returns: Returns True if the backup file was created successfully
    """
    state = col.create_backup(backup_folder=backup_folder, force=True,
                                 wait_for_completion=True)
    if not state:
        return False

    colpkg_file = find_colpkg_file(backup_folder)

    if compress_colpkg:
        subprocess.run(["gzip", backup_folder + "/" + colpkg_file])

    return True


def find_colpkg_file(dir_path: str) -> str:
    """Searches for a file with the colpkg extension in the path and returns its
    filename.

    :param dir_path: Path of the directory.
    :raises ValueError: If dir_path is not a directory.
    :returns: The filename of the first file that is finded.If it don't find any
        file, returns None.
    """
    if not os.path.isdir(dir_path):
        raise ValueError("dir_path is not a directory")

    pattern = re.compile(r".*.colpkg.*")
    for filename in os.listdir(dir_path):
        if pattern.match(filename):
            return filename
    return None


def backup_media(backup_folder: str, anki_user: str, compress_media: bool):
    """Copy the collection.media folder to the backup folder.

    :param backup_folder: Path of the directory where the media will be copied
    :param anki_user: Username of the current anki_user
    :param compress_media: If True, then all collection.media will be compressed
        with gzip command line tool
    """
    # Get the username of the current user
    user = subprocess.run("echo $USER", shell=True, capture_output=True,
                          text=True).stdout.strip()
    dir_images = "/home/" + user + "/.local/share/Anki2/" + anki_user + "/collection.media"

    # Only update the new files or the modified ones
    subprocess.run(["cp", "-ruv", dir_images, backup_folder])

    if compress_media:
        subprocess.run(["gzip", backup_folder + "/collection.media"])


def copy_to_remote(backup_folder: str, remote: str):
    """Syncronice all the content of the backup folder to remote

    :param backup_folder: Path of the backup directory
    :param remote: Name of the rclone remote
    """
    subprocess.run(["rclone", "sync", backup_folder, remote,
                    "--progress"])
