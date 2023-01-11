#!/usr/bin/env python3
import argparse
import shutil
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--glob", required=True)
    parser.add_argument("-i", "--input-path", required=True)
    parser.add_argument("-s", "--batch-size", help="In GB", required=True, type=int)
    parser.add_argument("-d", "--destination-prefix-path", required=True)
    parser.add_argument("--dry-run", required=False, default=False, action="store_true")
    args = parser.parse_args()
    batches = []
    if args.dry_run:
        print("Dry run not coping.")
    max_batch_size = args.batch_size * 1024 * 1024 * 1024
    print(max_batch_size)
    input_path = Path(args.input_path)
    files = sorted(
        [(f, f.stat().st_size) for f in list(input_path.glob(args.glob))],
        key=lambda x: x[0],
    )
    batch_size = 0
    batch = []
    for item_name, item_size in files:
        if batch_size + item_size < max_batch_size:
            batch_size += item_size
            batch.append(item_name)
        else:
            batches.append(batch)
            batch_size = item_size
            batch = [item_name]
    if len(batch) > 0:
        batches.append(batch)

    for batch_id, batch_items in enumerate(batches):
        batch_path = Path("{}_{}".format(args.destination_prefix_path, batch_id))
        batch_path.mkdir(parents=True, exist_ok=True)
        for batch_item in batch_items:
            print(
                "Copying {} to {}".format(
                    batch_item.absolute(),
                    batch_path.joinpath(batch_item.name).absolute(),
                )
            )
            if not args.dry_run:
                shutil.copy(
                    batch_item.absolute(),
                    batch_path.joinpath(batch_item.name).absolute(),
                )


if __name__ == "__main__":
    sys.exit(main())
