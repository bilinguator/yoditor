import os
import re
from tqdm import tqdm

"""
Uploading two lists of Russian words:
list `yo_sure` - words where <Ё> letter is 100% certain;
list `yo_unsure` - words with uncertianty about <Ё> letters.
"""

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
YO_SURE_PATH = os.path.join(SCRIPT_DIR, 'yobase/yo_sure.txt')
YO_UNSURE_PATH = os.path.join(SCRIPT_DIR, 'yobase/yo_unsure.txt')
YO_SURE_COLLOCATIONS_PATH = os.path.join(SCRIPT_DIR, 'yobase/yo_sure_collocations.txt')
YE_SURE_PATH = os.path.join(SCRIPT_DIR, 'yobase/ye_sure.txt')
YE_SURE_FIRST_WORDS_PATH = os.path.join(SCRIPT_DIR, 'yobase/ye_sure_first_words.txt')
SENTENCE_ENDS = '.,!?;–—…'
AFTER_WORD = SENTENCE_ENDS + ' '

assert os.path.isfile(YO_SURE_PATH), \
    f'\nFile with words always spelled with the <Ё> letter not found!' + \
    f'\nФайл со словами, которые всегда пишутся с буквой <Ё>, не найден!\n\033[1m{YO_SURE_PATH}\033[0m'
assert os.path.isfile(YO_UNSURE_PATH), \
    f'\nFile with words not always spelled with the <Ё> letter not found!' + \
    f'\nФайл со словами, которые не всегда пишутся с буквой <Ё>, не найден!\n\033[1m{YO_UNSURE_PATH}\033[0m'

with open(YO_SURE_PATH, 'r', encoding='UTF-8') as file:
    yo_sure = file.read().split()
with open(YO_UNSURE_PATH, 'r', encoding='UTF-8') as file:
    yo_unsure = file.read().split()


def replace_by_regex(text: str, regex: str, old: str, new: str) -> str:
    """
    Replace old substring to new one inside the hits found by regular expression.
    
    str `regex` - string with regular expression for searching hits by re.findall;
    str `old` - string to be replace inside the hits found by regex;
    str `new` - target replacement;
    return: str - text with replacements in the hits.
    """
    
    for hit in set(re.findall(regex, text)):
        hit_replace = hit.replace(old, new)
        text = text.replace(hit, hit_replace)
        
    return text


def get_words_with_ye(text: str) -> str:
    """
    Get all words of the text containing the Russian <е> letters.

    str `text` - text where to find words with the Russian <е> letters.

    return set of str - set of lower case words containing the Russian <е> letters.
    """

    text_words = re.findall(r'\b\w+\b', text.lower())
    return set([word for word in text_words if 'е' in word])


def yobase_text_intersection(yobase: list[str], text: str) -> list:
    """
    Find all potential words in the text to recover the <Ё> letters using Yobase.

    list of str `yobase` - words from Yobase;
    str `text` - text where to find words to recover the <Ё> letters.

    return list of str - potential words in which to recover the <Ё> letters.
    """

    text_words = get_words_with_ye(text)
    return [word for word in yobase
            if word.replace('ё', 'е') in text_words]


def recover_yo_sure_compound_adjective(text: str) -> str:
    """
    Recover the <Ё> letters in the first parts of the compound adjectives, e.g. "зелёно-синий".

    str `text` - text where to recover the <Ё> letters in the first parts of the compound adjectives.

    return str - text with the <Ё> letters recovered in the first parts of the compound adjectives.
    """

    with open('../yoditor/yobase/yo_sure_compound.txt', 'r', encoding='utf-8') as file:
        yo_sure_compound = [line.strip() for line in file.readlines()]
    
    for word in yo_sure_compound:
        for word in (word.lower(), word.upper(), word.capitalize()):
            word_with_ye = word.replace('ё', 'е').replace('Ё', 'Е')
            regex = rf'\b{word_with_ye}-\w+[{AFTER_WORD}]'
            text = replace_by_regex(text, regex, word_with_ye, word)

    return text


def escape_ye_sure_first_words(text: str) -> str:
    """
    Escape the <Е> letters in the words never used with prepositions.
    For example, "Я знаю, чем тебе помочь." becomes "Я знаю, ч<е>м тебе помочь.",
    because "чем" right after the comma is never written with the <Ё> letter.

    str `text` - text where to escape the <Е> letters.

    return str - text with the <Е> letters escaped.
    """
    
    with open(YE_SURE_FIRST_WORDS_PATH, 'r', encoding='utf-8') as file:
        ye_sure_first_words = [line.strip() for line in file.readlines()]

    for word in ye_sure_first_words:
        for word_with_escape in (word.lower(), word.upper(), word.capitalize()):
            word_wo_escape = word_with_escape.replace('<', '').replace('>', '')
            regex = rf'[{SENTENCE_ENDS}]\s{word_wo_escape}[{AFTER_WORD}]'
            text = replace_by_regex(text, regex, word_wo_escape, word_with_escape)

    return text


def escape_ye_sure(text: str) -> str:
    """
    Escape the <Е> letters in the words with angle brackets where this letter is obligatory.
    For example, "прежде чем" becomes "прежде ч<е>м", because this collocation is never written with <Ё>.
    This allows to esape a set of words from the process of recovering the <Ё> letters.

    str `text` - text where to escape the <Е> letters.

    return str - text with the <Е> letters escaped.
    """
    
    text = escape_ye_sure_first_words(text)

    with open(YE_SURE_PATH, 'r', encoding='utf-8') as file:
        ye_sure = [line.strip() for line in file.readlines()]
    
    for word in ye_sure:
        for word_with_escape in (word.lower(), word.upper(), word.capitalize()):
            word_wo_escape = word_with_escape.replace('<', '').replace('>', '')
            regex = rf'\s{word_wo_escape}[{AFTER_WORD}]'
            text = replace_by_regex(text, regex, word_wo_escape, word_with_escape)

    return text


def unescape_ye_sure(text: str) -> str:
    """
    Remove <Е> letters escaping.

    str `text` - text where to unescape the <Е> letters.

    return str - text with the <Е> letters unescaped.
    """
        
    return text.replace('<е>', 'е').replace('<Е>', 'Е')


def recover_yo_sure(text: str) -> str:
    """
    Recover all certain <Ё> in the text.
    
    str `text` - text where to find and recover certain <Ё> letters;
    return - str: text with certain <Ё> letters recovered.
    """
    
    text = recover_yo_sure_compound_adjective(text)

    yo_sure_words = yobase_text_intersection(yo_sure, text)

    with open(YO_SURE_COLLOCATIONS_PATH, 'r', encoding='utf-8') as file:
        yo_sure_words += [line.strip() for line in file.readlines()]

    for word in tqdm(yo_sure_words):
        for w_yo in (word.lower(), word.upper(), word.capitalize()):
            w_ye = w_yo.replace('ё', 'е').replace('Ё', 'Е')
            text = replace_by_regex(text, rf'\s{w_ye}[{AFTER_WORD}]', w_ye, w_yo)

    return text


def recover_yo_unsure(text: str, print_width: int=100, yes_reply: str='ё') -> str:
    """
    Recover all uncertain <Ё> in the text in the interaction mode.
    
    str `text` - text where to find and recover uncertain <Ё> letters;
    int `print_width` - how many characters to print while interaction (default: 100);
    str `yes_reply` - input required to confirm replacement <Е> with <Ё> (default: "ё");
    return - str: text with uncertain <Ё> letters recovered.
    """

    yo_unsure_words = yobase_text_intersection(yo_unsure, text)
    
    text = escape_ye_sure(text)

    for word in yo_unsure_words:
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
                printed_text = unescape_ye_sure(printed_text)
                cli_width = round(os.get_terminal_size().columns * 0.75)
                
                print('_' * cli_width)
                print(printed_text)

                if input(f'{word_with_ye} → {w}? ').lower() == yes_reply:
                    text = text[:start] + text[start:end].replace(word_with_ye, w) + text[end:]

    text = unescape_ye_sure(text)
    
    print('\n\033[1;31m<Ё> recovery complete!\033[0m')
    print('\033[1;31mРасстановка точек над <Ё> завершена!\033[0m')
    return text