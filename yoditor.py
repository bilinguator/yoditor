import os
import re
from tqdm import tqdm

"""Uploading two lists of Russian words:
list `yo_sure` - words where <Ё> letter is 100% certain;
list `yo_unsure` - words with uncertianty about <Ё> letters.
"""

script_dir = os.path.dirname(os.path.abspath(__file__))
yo_sure_path = os.path.join(script_dir, 'yobase/yo_sure.txt')
yo_unsure_path = os.path.join(script_dir, 'yobase/yo_unsure.txt')

assert os.path.isfile(yo_sure_path), \
    f'\nFile with words always spelled with the <Ё> letter not found!' + \
    f'\nФайл со словами, которые всегда пишутся с буквой <Ё>, не найден!\n\033[1m{yo_sure_path}\033[0m'
assert os.path.isfile(yo_unsure_path), \
    f'\nFile with words not always spelled with the <Ё> letter not found!' + \
    f'\nФайл со словами, которые не всегда пишутся с буквой <Ё>, не найден!\n\033[1m{yo_unsure_path}\033[0m'

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

def recover_yo_sure (text):
    """Recover all certain <Ё> in the text.
    
    str `text` - text where to find and recover certain <Ё> letters;
    return - str: text with certain <Ё> letters recovered.
    """
    for i, word in enumerate(tqdm(yo_sure)):
        for w_yo in {word.lower(), word.upper(), word.capitalize()}:
            w_ye = w_yo.replace('ё', 'е').replace('Ё', 'Е')
            text = replace_by_regex(text, rf'\b{w_ye}\b', w_ye, w_yo)
    return text

def recover_yo_unsure (text, print_width=100, yes_reply='ё'):
    """Recover all uncertain <Ё> in the text in the interaction mode.
    
    str `text` - text where to find and recover uncertain <Ё> letters;
    int `print_width` - how many characters to print while interaction (default: 100);
    str `yes_reply` - input required to confirm replacement <Е> with <Ё>;
    return - str: text with uncertain <Ё> letters recovered.
    """
    for word in yo_unsure:
        for w in [word, word.capitalize(), word.upper()]:
            word_with_ye = w.replace('ё', 'е').replace('Ё', 'Е')

            hits = re.finditer(rf'\b{word_with_ye}\b', text)
            for hit in hits:
                start = hit.start()
                end = hit.end()
                hit_len = end - start
                print_start = max(0, start - print_width // 2 + hit_len // 2 + hit_len % 2)
                print_end = min(len(text), end + print_width // 2 - hit_len // 2)
                
                start_diff = start - print_start
                end_diff = print_end - end
                print_sum = start_diff + end_diff + hit_len
                
                if end_diff < start_diff and print_sum < print_width:
                    print_start = max(0, print_start - (print_width - print_sum))
                if end_diff > start_diff and print_sum < print_width:
                    print_end = min(len(text), print_end + (print_width - print_sum))
                
                printed_text = f'\n{text[print_start:start]}\033[1;31m{text[start:end]}\033[0m{text[end:print_end]}\n'
                cli_width = round(os.get_terminal_size().columns * 0.75)
                
                print('_' * cli_width)
                print(printed_text)

                if input(f'{word_with_ye} → {w}? ').lower() == yes_reply:
                    text = text[:start] + text[start:end].replace(word_with_ye, w) + text[end:]
    print('\n\033[1;31m<Ё> recovery complete!\033[0m')
    print('\033[1;31mРасстановка точек над <Ё> завершена!\033[0m')
    return text