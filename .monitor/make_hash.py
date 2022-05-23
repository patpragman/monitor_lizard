# hash a file without opening the whole file

import hashlib


def hash_file(path, buffer=2**16) -> str:
    md5 = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            data = f.read(buffer)
            if not data:
                break
            md5.update(data)

    return md5.hexdigest()