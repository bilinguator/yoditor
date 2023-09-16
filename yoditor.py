import os

"""Uploading two lists of Russian words:
`yo_sure` - words where <Ё> letter is 100% certain;
`yo_unsure` - words with uncertianty about <Ё> letters.
"""

yo_sure_path = 'yobase/yo_sure.txt'
yo_unsure_path = 'yobase/yo_unsure.txt'

assert os.path.isfile(yo_sure_path), \
    'File with words certain about <Ё> (\033[1m{}\033[0m) not found!'.format(yo_sure_path)
assert os.path.isfile(yo_unsure_path), \
    'File with words uncertain about <Ё> (\033[1m{}\033[0m) not found!'.format(yo_unsure_path)

with open(yo_sure_path, 'r', encoding='UTF-8') as file:
    yo_sure = file.read().split()
with open(yo_unsure_path, 'r', encoding='UTF-8') as file:
    yo_unsure = file.read().split()