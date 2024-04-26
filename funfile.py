# def recursive_items(dictionary, path='', start=''):
#     for key, value in dictionary.items():
#         new_path = f'{path}/{key}' if path else key
#         if isinstance(value, dict):
#             # If the dictionary has any nested dictionaries, don't print the current path
#             if any(isinstance(v, dict) for v in value.values()):
#                 recursive_items(value, new_path)
#             else:
#                 print(new_path)
#         else:
#             continue
#
# metadata = {'another_folder': {"another_file": {"nothing": 1}},
#      'folder': {'type': "file", "file": {"inside_file":{"type":"a"}},
#                 "more": 2, 3: 4, "file_f": {"5": 6}},
#                     'file_d': {1: 2, 3: 4}, 'file_b': {5: 6}}
#
# recursive_items(metadata)

def recursive_items(dictionary, path='', start=''):
    for key, value in dictionary.items():
        new_path = f'{path}/{key}' if path else key
        if isinstance(value, dict):
            # If the dictionary has any nested dictionaries, don't print the current path
            if any(isinstance(v, dict) for v in value.values()):
                recursive_items(value, new_path, start)
            elif new_path.startswith(start):
                print(new_path)
        else:
            continue

possible_moves = "hey"


if "sdfheyo".startswith(possible_moves):
    print("yes")
else:
    print("no")



