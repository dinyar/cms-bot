#!/bin/env python3
from os.path import basename
from sys import argv, exit
from json import loads, dumps

try:
    authors_info = {}
    repo = argv[1]
    err, output = subprocess.getstatusoutput(
        "curl -s https://api.github.com/repos/" + repo + "/stats/contributors"
    )
    if err:
        print(output)
        exit(1)
    data = loads(output)
    for item in data:
        authors_info[item["author"]["login"]] = item["total"]
    if not authors_info:
        print(output)
        exit(1)
    print(
        basename(repo).upper().replace("-", "_")
        + "_AUTHORS="
        + dumps(authors_info, sort_keys=True, indent=2)
    )
except IndexError:
    print("Repo Name Required ... Arugement missing !!!!")
    exit(1)
