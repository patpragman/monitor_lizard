#!/usr/bin/env python3.9

import os
from pathlib import Path
import pickle
from ignorer import ignore_list
from check import is_ignored
from make_hash import hash_file
from backup import create_backup, delete_file
from datetime import datetime
import logging
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--backup",
                        help="create a backup of the files in this directory",
                        default=True,
                        action="store_true")

    parser.add_argument("--target_directory",
                        help="location of the backup",
                        default=".backup",
                        type=str)

    parser.add_argument("--deleted_directory",
                        help="location of the backup",
                        default=".deleted",
                        type=str)

    args = parser.parse_args()

    backup_path = args.target_directory
    deleted_path = args.deleted_directory

    now = datetime.utcnow()
    format = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(filename=".change_log.log",
                        encoding='utf-8',
                        level=logging.INFO)

    # load the previous hash_dict, if you can't find one, make a new dictionary
    try:
        old_hashes = pickle.load(open(".state.p", "rb"))
    except FileNotFoundError:
        logging.warning(f'{now.strftime(format)} - no previous .state.p found, not able to register any change.')
        old_hashes = {}

    # get where you're running the file, and get the backup directory
    running_location = os.getcwd()
    path = str(Path(running_location).parent)
    backup_directory = f"{path}/{backup_path}"
    deleted_directory = f"{path}/{deleted_path}"

    current_hashes = {}
    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        if is_ignored(dirpath, ignore_list):
            # we want to skip things that are to be ignored
            continue
        else:
            # here's where the magic happens - we need to read open that file, then get the hash

            for file in filenames:
                file_path = f"{dirpath}/{file}"
                current_hashes[file_path] = hash_file(file_path)

    delete_list = []
    # first let's look fore files that have been deleted
    for file in old_hashes:
        # if a file is in the old hashes but not in the new hashes, it's been deleted
        if file not in current_hashes:
            logging.info(f"{now.strftime(format)} - {file} has been deleted")
            delete_list.append(file)

    update_list = []
    for file in current_hashes:
        if file in old_hashes:
            if old_hashes[file] == current_hashes[file]:
                pass
            else:
                # change is detected
                logging.info(f"{now.strftime(format)} - {file} has changed")
                update_list.append(file)
        else:
            # it's a new file, so note that
            logging.info(f"{now.strftime(format)} - new file found {file}")
            update_list.append(file)

    for file in update_list:
        create_backup(file, local_backup_path=backup_directory)

    for file in delete_list:
        delete_file(file,
                    local_backup_path=backup_directory,
                    deleted_folder=deleted_directory)

    # finally save the pickle file
    pickle.dump(current_hashes, open(".state.p", "wb"))