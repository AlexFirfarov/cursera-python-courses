import argparse
import tempfile
import json
import os
from collections import OrderedDict

parser = argparse.ArgumentParser()
parser.add_argument("--key", type=str)
parser.add_argument("--val", type=str, default=None)
args = parser.parse_args()
storage_path = os.path.join(tempfile.gettempdir(), "storage.data")

dictionary = OrderedDict()

with open(storage_path, 'a') as f:
    pass
empty = os.stat(storage_path).st_size == 0

if args.val is not None:
    with open(storage_path, 'r') as f:
        if not empty:
            dictionary = json.load(f)
    with open(storage_path, 'w') as f:
        if args.key in dictionary:
            dictionary[args.key].append(args.val)
        else:
            dictionary[args.key] = [args.val]
        json.dump(dictionary, f)
else:
    with open(storage_path , 'r') as f:
        if not empty:
            dictionary = json.load(f)
            if args.key in dictionary:
                print(', '.join(dictionary[args.key]))
            else:
                print("None")
        else:
            print("None")
