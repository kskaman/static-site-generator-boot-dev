import os
import shutil

def copy_static_to_public(src="static", dest="public") -> None:
    """
    Copies all files from the source directory to the destination directory.
    If the destination directory exists, it will be removed before copying.
    """

    # Remove destination directory if it exists
    if os.path.exists(dest):
        print(f"Removing existing directory: {dest}")
        shutil.rmtree(dest)
    
    # Create destination directory
    os.mkdir(dest)

    # Walk through source directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"Copied file: {src_path} → {dest_path}")
        else:
            # Recursively copy subdirectory
            print(f"Entering directory: {src_path}")
            copy_static_to_public(src_path, dest_path)
