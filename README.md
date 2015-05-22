Python module for shorting long key names. Returns new dict with replaced keys and dict with pairs "old key" : "new key". Useful for sending big JSONs by net.

Example:

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

Increase object and you'll see more difference.