# returns true if it's ignored
def is_ignored(file_path:str, ignore_list: list[str]) -> bool:

    for ignorable in ignore_list:
        if ignorable in file_path:
            return True

    return False