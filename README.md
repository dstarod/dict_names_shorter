Python class for shorting long key names. Returns new dict with replaced keys and dict with pairs "new key" : "old key". Useful for sending big JSONs by net.

Example:

    import json

    with open('example.json') as f:
        d = json.load(f)

    print(len(json.dumps(d)))  # 9327

    shorter = DictNamesShorter()
    
    # Make keys shorter
    shorten_dict, replaced_names = shorter.modify(d)    
    shorten_json_len = len(json.dumps(shorten_dict))  # 5682
    replaced_json_len = len(json.dumps(replaced_names))  # 1586
    print(shorten_json_len + replaced_json_len)  # 7268

    # Restore keys
    restored_dict, replaced_names = shorter.modify(shorten_dict, replaced_names)    

Increase object and you'll see more difference.


