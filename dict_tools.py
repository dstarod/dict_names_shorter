__author__ = 'Dmitry Starodubtsev'
__email__ = "dmitry.starodubcev@gmail.com"
__license__ = "GPL"
__date__ = '2015-05-21'
__version__ = '0.1'

from itertools import chain
from types import GeneratorType


def names_generator():
    """ Generate short names """
    available = 'abcdefghijklmnopqrstuvwxwzABCDEFGHIJKLMNOPQRSTUVWXWZ0123456789'
    l1_aliases = (a for a in available)
    l2_aliases = (a+b for a in available for b in available)
    l3_aliases = (a+b+c for a in available for b in available for c in available)
    l4_aliases = (a+b+c+d for a in available for b in available for c in available for d in available)
    l5_aliases = (a+b+c+d+e for a in available for b in available for c in available for d in available for e in available)
    for alias in chain(l1_aliases, l2_aliases, l3_aliases, l4_aliases, l5_aliases):
        yield alias


def names_replace(doc, aliases=None, repl={}):
    """ Replace dict key names by repl map if exists, or get new short name from aliases generator """
    if type(doc) == dict:
        new_dict = {}
        for key, item in doc.items():
            if key not in repl:
                if not aliases or type(aliases) != GeneratorType:
                    raise ValueError('Need aliases generator ')
                try:
                    new_key = aliases.next()
                    repl[key] = new_key
                except StopIteration:
                    raise RuntimeError('Too many keys for shorting, sorry')
            
            if type(item) in (tuple, list, dict):
                item, repl = names_replace(item, aliases, repl)

            new_key = repl[key]
            new_dict[new_key] = item
        return new_dict, repl

    elif type(doc) in (tuple, list):
        new_list = []
        for item in doc:
            if type(item) in (list, dict):
                item, repl = names_replace(item, aliases, repl)
            new_list.append(item)
        return type(doc)(new_list), repl

    else:
        return doc, repl


if __name__ == '__main__':
    import json
    from dict_tools import names_generator, names_replace

    with open('example.json') as f:
        doc = json.load(f)

    # Original JSON length
    print(len(json.dumps(doc)))  # 9327

    # Generator for short names
    aliases = names_generator()
    
    # New dict with replaced key names and dict with replace map {'old': 'new'}
    shorten, replaced = names_replace(doc, aliases=aliases)

    # Check new JSONs size : 7322
    print(len(json.dumps(shorten)))  # 5682
    print(len(json.dumps(replaced)))  # 1640

    # Restore original names : switch new and old key names
    reverced_keys = {v: k for k, v in replaced.items()}
    restored_dict, replaced_names =  names_replace(shorten, repl=reverced_keys)
