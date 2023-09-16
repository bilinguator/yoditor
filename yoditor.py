import os
import re

"""Uploading two lists of Russian words:
list `yo_sure` - words where <Ё> letter is 100% certain;
list `yo_unsure` - words with uncertianty about <Ё> letters.
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

def replace_by_regex (text, regex, old, new):
    """Replace old substring to new one inside the hits found by regular expression.
    
    str `regex` - string with regular expression for searching hits by re.finditer;
    str `old` - string to be replace inside the hits found by regex;
    str `new` - target replacement;
    return: str - text with replacements in the hits.
    """
    hits = re.finditer(regex, text)
    for hit in hits:
        start = hit.start()
        end = hit.end()
        text = text[:start] + text[start:end].replace(old, new) \
            + text[end:]
    return text