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
        from itertools import chain
        l1_aliases = (a for a in 'abcdefghijklmnopqrstuvwxwzABCDEFGHIJKLMNOPQRSTUVWXWZ0123456789')
        l2_aliases = (a+b for a in l1_aliases for b in l1_aliases)
        l3_aliases = (a+b for a in l2_aliases for b in l1_aliases)
        l4_aliases = (a+b for a in l2_aliases for b in l2_aliases)
        for alias in chain(l1_aliases, l2_aliases, l3_aliases, l4_aliases):
            yield alias

    def walk(self, doc):
        if type(doc) == dict:
            new_dict = {}
            for key, item in doc.items():
                if key not in self.short_keys:
                    try:
                        new_key = self.alias.next()
                    except StopIteration:
                        raise RuntimeError('Too many keys for shorting, sorry')
                self.short_keys[key] = new_key

                if type(item) in (tuple, list, dict):
                    item = self.walk(item)
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

    d = {'text': 'Text', 'items': (1, 2, 3), 'obj': ({'item1': 1, 'item2': 2}, {'item3': 3})}
    print(len(json.dumps(d)))

    shorter = DictNamesShorter()
    d, n = shorter.short(d)
    print(d, n)
    print(len(json.dumps(d)))
