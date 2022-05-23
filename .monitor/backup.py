# creates a backup in the appropriate .backup folder
# the path of which is specified here
import os
import shutil

def create_backup(path,
                  local_backup_path: str = ".backup"):

    local_backup_path = f"{local_backup_path}{path}"

    # backup locally
    print(f'Backing up {path} -> {local_backup_path}')
    target = "/".join(local_backup_path.split("/")[0:-1])
    os.makedirs(target, exist_ok=True)
    shutil.copy(path, target)

def delete_file(path,
                local_backup_path: str = ".backup",
                deleted_folder: str =".deleted"):
    # we soft delete everything here, we move the deleted file to the .deleted folder
    local_backup_path = f"{local_backup_path}{path}"
    shutil.copy(local_backup_path, deleted_folder)
    os.remove(local_backup_path)