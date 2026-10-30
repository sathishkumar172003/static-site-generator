import shutil
import os 

LOG_FILE = os.path.join(os.getcwd(), "clean-file.log")

def log_message(message: str):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")
    return True 


def cleanDir(dir_path: str) -> bool:
    """
    deletes all the files and directories inside the provided directory.
    args:
        dir_path: path to the directory to be cleaned
    returns:
        boolean: True if the directory was cleaned successfully, False otherwise
    """
    path_exists = os.path.exists(dir_path)
    if not path_exists:
        return False
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
            return False
    return True

def copyDir(src: str, dest: str) -> bool:
    """
    copies all the files and directories from the source directory to the destination directory.
    args:
        src: path to the source directory
        dest: path to the destination directory
    returns:
        boolean: True if the directory was copied successfully, False otherwise
    """
    if not os.path.exists(src):
        print(f"Source directory does not exist: {src}")
        return False

    if not os.path.exists(dest):
        os.makedirs(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        try:
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dest_path)
                log_message(f"File copied: {src_path} -> {dest_path}")
            elif os.path.isdir(src_path):
                copyDir(src_path, dest_path)
        except Exception as e:
            print(f'Failed to copy {src_path} to {dest_path}. Reason: {e}')
            log_message(f"Failed to copy: {src_path} -> {dest_path}. Reason: {e}")
            return False
    return True
