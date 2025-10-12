# Downloads Folder Cleanup Script

This script automatically deletes (or simulates deleting) files in a folder that haven’t been accessed in a specified number of months.  
It’s useful for keeping your **Downloads** directory organized and uncluttered.

---

## Features

- Deletes or safely sends files to the **Recycle Bin** (via `send2trash`)
- Supports **dry-run mode** to preview what would be deleted
- Optional **logging** of deletions to a log file
- Simple to customize — you can adjust the folder path and retention period

---

## Usage

 - Replace the path to donwloads folder by your own
 - Run the script in your terminal or IDE
 - By default, dry run is set to True, if you want to dele your files, just set it to False
