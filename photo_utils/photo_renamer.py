#!/usr/bin/env python3
import argparse
import os
import os.path
import re
import shutil
import sys
from pathlib import Path

get_id = re.compile(r"PICT(?P<id>\d+)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-path", required=True)
    parser.add_argument("-d", "--destination-path", required=True)
    parser.add_argument("-s", "--since", required=True, type=int)
    parser.add_argument("--dry-run", required=False, default=False, action="store_true")
    args = parser.parse_args()

    print(
        "Input path: {}. Copying since id: {} to destination path: {}".format(
            args.input_path, args.since, args.destination_path
        )
    )

    if args.dry_run:
        print("Dry run not coping.")

    Path(args.destination_path).mkdir(parents=True, exist_ok=True)
    input_path = Path(args.input_path)
    files = [x for x in input_path.iterdir() if x.is_file()]
    for old_file in files:
        matched = get_id.match(old_file.name)
        if matched:
            old_id = int(matched.group(1))
            if old_id > args.since:
                new_id = old_id - args.since
                new_file = os.path.join(args.destination_path, f"PICT{new_id:04d}.JPG")
                print("Copying {} to {}".format(old_file.absolute(), new_file))
                if not args.dry_run:
                    shutil.copyfile(old_file, new_file)


if __name__ == "__main__":
    sys.exit(main())
