#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from pprint import pprint


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--first-path", required=True)
    parser.add_argument("-s", "--second-path", required=True)

    args = parser.parse_args()
    print("Comparing paths: {} and {}".format(args.first_path, args.second_path))

    first_path = Path(args.first_path)
    first_path_rolls = set([x.name for x in first_path.iterdir() if x.is_dir()])

    second_path = Path(args.second_path)
    second_path_rolls = set([x.name for x in second_path.iterdir() if x.is_dir()])

    print("Directories of {} missing in {}:".format(args.first_path, args.second_path))
    pprint(first_path_rolls.difference(second_path_rolls))

    print("Directories of {} already in {}:".format(args.first_path, args.second_path))
    print(" ".join(list(first_path_rolls.intersection(second_path_rolls))))


if __name__ == "__main__":
    sys.exit(main())
