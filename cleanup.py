import logging
from pathlib import Path
from send2trash import send2trash
from datetime import datetime, timedelta

PATH_TO_DOWNLOADS = r"C:/Users/delga/Downloads"

def setup_logging(log_file: str = None):
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


def validate_folder(folder: str):
    """
    Check if the given folder path exists.
    folder : str -> Path to the folder to validate.
    Returns a Path -> A Path object for the validated folder.
    Raises a FileNotFoundError -> If the folder does not exist.
    """
    folder_path = Path(folder)
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder {folder} does not exist")
    return folder_path


def process_file(file: Path, cutoff: datetime, dry_run: bool = True):
    """
    Delete or simulate deleting a file if it hasn't been accessed since cutoff date.
    file : Path -> File to process.
    cutoff : datetime -> Date threshold for deletion.
    dry_run : bool, optional -> If True, only simulate deletion (default is True).
    Returns a bool True if file was deleted (or would be deleted), False otherwise.
    """
    try:
        if file.is_file():
            last_access = datetime.fromtimestamp(file.stat().st_mtime)
            # Check if file is older than the cutoff
            if last_access < cutoff:
                if dry_run:
                    print(f"[DRY RUN] Would delete: {file} | last accessed: {last_access}")
                else:
                    send2trash(file)  # Safer than os.remove(), can be recovered from trash
                    print(f"Deleting file: {file}")
                    logging.info(f"Deleted: {file}")
                    return True

    except Exception as e:
        print(f"Error processing {file}: {e}")
        logging.error(f"Error processing {file}: {e}")
    return False


def cleanup_downloaded_files(folder: str, months: int, dry_run: bool = True, log_file: str = None):
    """
    Clean up old files in a specified folder.
    folder : str -> Folder to scan and clean.
    months : int -> Delete files not accessed for this many months.
    dry_run : bool, optional -> If True, simulate deletions without removing files (default is True).
    log_file : str, optional -> Path to a log file. If provided, logs are saved there.
    """
    setup_logging(log_file)

    try:
        folder_path = validate_folder(folder)
    except FileNotFoundError as e:
        print(e)
        return

    cutoff = datetime.now() - timedelta(days=30 * months)
    deleted_count = 0

    # Iterate through all files in the folder
    for file in folder_path.iterdir():
        if process_file(file, cutoff, dry_run):
            deleted_count += 1

    print(f"Cleanup completed. Total files deleted: {deleted_count}"
          if not dry_run else "Dry run finished")


if __name__ == "__main__":
    cleanup_downloaded_files(folder=PATH_TO_DOWNLOADS, months=3, dry_run=True, log_file="cleanups.log")
