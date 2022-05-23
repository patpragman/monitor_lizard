# Script parses the ignore file and creates list of files to ignore

ignore_list = []
with open(".liz_ignore.txt") as ignore_file:

    # iterate through the lines in the ignore file, ignore everything after the # symbol
    for line in ignore_file.readlines():
        ignore = line.partition("#")[0].strip()
        if ignore != "":
            ignore_list.append(ignore)