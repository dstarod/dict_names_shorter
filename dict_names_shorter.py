__author__ = 'Dmitry Starodubtsev'
__email__ = "dmitry.starodubcev@gmail.com"
__license__ = "GPL"
__date__ = '2015-05-21'
__version__ = '0.1'


class DictNamesShorter:
    """
    Returns new dict with replaced keynames from original to short aliases.
    """
    def __init__(self):
        self.short_keys = {}
        self.alias = self.aliases()

    def aliases(self):
        from itertools import chain, tee
        from copy import copy
        available = 'abcdefghijklmnopqrstuvwxwzABCDEFGHIJKLMNOPQRSTUVWXWZ0123456789'
        l1_aliases = (a for a in available)
        l2_aliases = (a+b for a in available for b in available)
        l3_aliases = (a+b+c for a in available for b in available for c in available)
        l4_aliases = (a+b+c+d for a in available for b in available for c in available for d in available)
        l5_aliases = (a+b+c+d+e for a in available for b in available for c in available for d in available for e in available)
        for alias in chain(l1_aliases, l2_aliases, l3_aliases, l4_aliases, l5_aliases):
            yield alias

    def walk(self, doc):
        if type(doc) == dict:
            new_dict = {}
            for key, item in doc.items():
                if key not in self.short_keys:
                    try:
                        new_key = self.alias.next()
                        self.short_keys[key] = new_key
                    except StopIteration:
                        raise RuntimeError('Too many keys for shorting, sorry')
                
                if type(item) in (tuple, list, dict):
                    item = self.walk(item)

                new_key = self.short_keys[key]
                new_dict[new_key] = item
            return new_dict

        elif type(doc) in (tuple, list):
            new_list = []
            for item in doc:
                if type(item) in (list, dict):
                    item = self.walk(item)
                new_list.append(item)
            return type(doc)(new_list)

        else:
            return doc

    def short(self, doc):
        doc = self.walk(doc)
        new_dict = dict(zip(self.short_keys.values(), self.short_keys.keys()))
        return doc, new_dict


if __name__ == '__main__':
    import json

    with open('example.json') as f:
        d = json.load(f)

    print(len(json.dumps(d)))  # 9327

    shorter = DictNamesShorter()
    shorten_dict, replaced_names = shorter.short(d)
    shorten_json_len = len(json.dumps(shorten_dict))  # 5682
    replaced_json_len = len(json.dumps(replaced_names))  # 1586
    print(shorten_json_len + replaced_json_len)  # 7268
