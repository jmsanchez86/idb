#!/usr/local/bin/python3.5

"""
Requires Python 3.5

Sypnosis:
    ./collect.py directory_name

    Collects a lot of json files in a directory into one big json file called
    directory_name.json.

The output file contents will be a large dictionary with id as the key and
the json data as the value.

i.e.

recipes/
    1234.json
    999.json
    1112123.json

Will become:

recipes.json:
{
    "1234": {
        ...
    },
    "999": {
        ...
    },
    "1112123" {
        ...
    },
}

"""

import sys
import json
import re
from pathlib import Path

if __name__ == "__main__":
    args = sys.argv

    assert(len(args) == 2)

    path = Path(args[1])
    assert(path.exists())
    assert(path.is_dir())

    filename = path.name + ".json"
    filedata = dict()

    for f in path.glob("*.json"):
        fname = re.search("(.+)\.json", f.name).group(1)
        data = json.loads(f.read_text())
        # JSON indexes cannot be numerical so we leave fname as a str.
        filedata[fname] = data

    print("write to: " + filename)
    with open(filename, "w") as f:
        f.write(json.dumps(filedata, sort_keys=True, indent=4))





