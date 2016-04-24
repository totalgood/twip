from __future__ import absolute_import, print_function, unicode_literals
import os
import json
import settings


RAW_DATA_DIR = 'raw/'


def load_statuses(filename):
    name, ext = os.path.splitext(filename)
    if ext != '.json':
        return []

    with open(RAW_DATA_DIR + filename, 'r') as f:
        statuses = json.loads(f.read())

    return statuses


def merge():
    all_data = []
    filenames = os.listdir(RAW_DATA_DIR)
    for filename in filenames:
        statuses = load_statuses(filename)
        all_data.extend(statuses)

    with open(settings.MERGED_DATA_LOCATION, 'w') as f:
        f.write(json.dumps(all_data, indent=2))


if __name__ == '__main__':
    merge()
