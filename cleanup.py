import os
import logging
from pathlib import Path
from send2trash import send2trash
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
PATH_TO_DOWNLOADS = os.getenv("ROOT")# or r"C:/Users/delga/Downloads"


def setup_logging(log_file: str | None = None) -> None:
    """
    Configure logging settings.
    log_file : str, optional -> Path to the log file. If not provided, logs are not written to file.
    """
    if log_file:
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )


def validate_folder(folder: str) -> Path:
    folder_path = Path(folder)
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder {folder} does not exist")
    return folder_path


def process_file(file: Path, cutoff: datetime, dry_run: bool = True):
    """
    Delete or simulate deleting a file if it hasn't been modified since cutoff date.
    cutoff : datetime -> Date threshold for deletion.
    dry_run : bool -> If True, only simulate deletion (default is True).
    """
    try:
        if file.is_file():
            last_access = datetime.fromtimestamp(file.stat().st_mtime)

            if last_access < cutoff:
                if dry_run:
                    print(f"[DRY RUN] Would delete file: {file} | last modified: {last_access}")
                    return False
                else:
                    send2trash(file)
                    print(f"Deleting file: {file}")
                    logging.info(f"Deleted file: {file}")
                    return True

    except Exception as e:
        print(f"Error processing {file}: {e}")
        logging.error(f"Error processing {file}: {e}")
    return False


def process_directory(directory: Path, cutoff: datetime, dry_run: bool = True):
    """
    Delete or simulate deleting a directory if it hasn't been modified since cutoff date.
    WARNING: This will send the ENTIRE directory (and its contents) to trash.
    """
    try:
        if directory.is_dir():
            last_access = datetime.fromtimestamp(directory.stat().st_mtime)

            if last_access < cutoff:
                if dry_run:
                    print(f"[DRY RUN] Would delete directory: {directory} | last modified: {last_access}")
                    return False
                else:
                    send2trash(directory)
                    print(f"Deleting directory: {directory}")
                    logging.info(f"Deleted directory: {directory}")
                    return True

    except Exception as e:
        print(f"Error processing {directory}: {e}")
        logging.error(f"Error processing {directory}: {e}")
    return False


def cleanup_downloaded_files(folder: str, months: int, dry_run: bool = True, log_file: str = None):
    setup_logging(log_file)

    try:
        folder_path = validate_folder(folder)
    except FileNotFoundError as e:
        print(e)
        return

    cutoff = datetime.now() - timedelta(days=30 * months)
    deleted_files = 0
    deleted_dirs = 0

    for item in folder_path.iterdir():
        if item.is_file():
            if process_file(item, cutoff, dry_run):
                deleted_files += 1
        elif item.is_dir():
            if process_directory(item, cutoff, dry_run):
                deleted_dirs += 1

    if dry_run:
        print("Dry run finished")
    else:
        print(f"Cleanup completed. Files deleted: {deleted_files} | Directories deleted: {deleted_dirs}")


if __name__ == "__main__":
    cleanup_downloaded_files(folder=PATH_TO_DOWNLOADS, months=3, dry_run=True, log_file="cleanups.log")