import os
import time
import logging
import argparse
from pathlib import Path
import shutil
from send2trash import send2trash
from datetime import datetime, timedelta
PATH_TO_DOWNLOADS = r"C:/Users/delga/Downloads"


def setup_logging(log_file: str=None):
   if log_file: 
        logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
   
        
def validate_folder(folder: str):
    folder_path = Path(folder)
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder {folder} does not exist")
    return folder_path


def process_file(file: Path, cutoff: datetime, dry_run: bool=True):
    try:
        if file.is_file():
            last_access = datetime.fromtimestamp(file.stat().st_atime)
            if last_access < cutoff:
                if dry_run:
                    print(f"[DRY RUN] Would delete: {file} | last accessed: {last_access}")
                else:
                    send2trash(file)
                    print(f"Deleting file: {file}")
                    logging.info(f"Deleted: {file}")
                    return True
    
    except Exception as e:
        print(f"Error processing {file}: {e}")
        logging.error(f"Error processing {file}: {e}")
    return False


def cleanup_downloaded_files(folder: str, months: int, dry_run: bool=True, log_file: str=None):
    setup_logging(log_file)
    try:
        folder_path = validate_folder(folder)
    except FileNotFoundError as e:
        print(e)
        return
    
    cutoff = datetime.now() - timedelta(days=30 * months)
    deleted_count = 0
    for file in folder_path.iterdir():
        if process_file(file, cutoff, dry_run):
            deleted_count += 1
    print(f"Cleanup completed. Total files deleted: {deleted_count}" if not dry_run else "Dry run finished")
                    
                    
if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Clean up old files from Downloads folder")
    # parser.add_argument("--folder", default=str(Path.home() / "Downloads"))
    # parser.add_argument("--months", type=int, default=3, help="Delete files not opened in N months")
    # parser.add_argument("--dry-run", action="store_true", help="Preview without deleting")
    # parser.add_argument("--log", type=str, help="Optional log file to record actions")
    # args = parser.parse_args()
    
    # cleanup_downloaded_files(args.folder, args.months, args.dry_run, args.log)
    cleanup_downloaded_files(folder=PATH_TO_DOWNLOADS, months=3, dry_run=True, log_file="cleanups.log")
    