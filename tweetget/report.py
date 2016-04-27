from __future__ import absolute_import, print_function, unicode_literals
import os
import json
import settings


def report():
    if not os.path.isfile(settings.MERGED_DATA_LOCATION):
        print('No data to report on! Please run the merge script then run this!')

    with open(settings.MERGED_DATA_LOCATION, 'r') as f:
        tweets = json.loads(f.read())

    print()

    id_list = [t['id'] for t in tweets]
    print('Total tweets: {}'.format(len(id_list)))

    id_dict = {t['id']: t for t in tweets}
    id_set = set(id_dict.keys())
    print('Total unique tweets: {}'.format(len(id_set)))

    max_id = max(id_set)
    print('Newest id: {}'.format(max_id))

    min_id = min(id_set)
    print('Oldest id: {}'.format(min_id))

    max_date = id_dict[max_id]['created_at']
    print('Newest date: {}'.format(max_date))

    min_date = id_dict[min_id]['created_at']
    print('Oldest date: {}'.format(min_date))

    print()


if __name__ == '__main__':
    report()
