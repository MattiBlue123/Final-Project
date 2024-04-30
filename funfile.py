metadata = {
"root": {
    "type": "directory",
    "children": {
        "file1.txt": {
            "type": "file",
            "pointer": 0,
            "size": 1000
        },
        "dir1": {
            "type": "directory",
            "children": {
                "file2.txt": {
                    "type": "file",
                    "pointer": 1000,
                    "size": 2000
                },
                "file3.txt": {
                    "type": "file",
                    "pointer": 3000,
                    "size": 1500
                }
            }
        },
        "dir2": {
            "type": "directory",
            "children": {
                "file4.txt": {
                    "type": "file",
                    "pointer": 4500,
                    "size": 2500
                }
            }
        }
    }
}
}
metadata = str(metadata)

string = '{"a": 1, "b": "2", "c": "hi"}'
# def from_string_to_nested_dict(basic_dict_string, output_dict=dict(),
#                                data = []):
#     if output_dict == {}:
#         basic_dict_string= basic_dict_string[1:-1]
#     for i in basic_dict_string:
#         if i == "{":
#             a = None
#             count = 0
#             while a != "}":
#
#
#             basic_dict_string
#
#         if i == ":"
#
# #
#
# def parse_dict(string):
#     stack = []
#     result = {}
#     key = None
#     value = ''
#     in_quotes = False
#
#     for char in string:
#         if char == '{':
#             if key is not None:
#                 stack.append((result, key))
#                 result[key] = {}
#                 result = result[key]
#                 key = None
#         elif char == '}':
#             if value:
#
#                 result[key] = value.strip()
#
#                 value = ''
#             if stack:
#                 result, key = stack.pop()
#         elif char == '"':
#             in_quotes = not in_quotes
#         elif char == ':' and not in_quotes:
#             key = value.strip('"')
#             value = ''
#         elif char == ',' and not in_quotes:
#             if value:
#
#                 result[key] = value.strip()
#                 if value.isdigit():
#                     value = int(value)
#                 value = ''
#         else:
#             value += char
#
#     if key is not None and value:
#         result[key] = value.strip()
#
#     return result
#
# string = '{"a":1,"b":2,"C":"3","d":{"hey":None,"yes":4}}'
# result_dict = parse_dict(string)
# print(result_dict)
#

def parse_dict(string):
    stack = []
    result = {}
    key = None
    value = ''
    in_quotes = False

    for char in string:
        if char == '{':
            if key is not None:
                stack.append((result, key.strip()))
                result[key.strip()] = {}
                result = result[key.strip()]
                key = None
        elif char == '}':
            if value:
                result[key.strip()] = value.strip()
                value = ''
            if stack:
                result, key = stack.pop()
        elif char == '"':
            in_quotes = not in_quotes
        elif char == ':' and not in_quotes:
            key = value.strip('"')
            value = ''
        elif char == ',' and not in_quotes:
            if value:
                result[key.strip()] = value.strip()
                value = ''
        else:
            value += char

    if key is not None and value:
        result[key.strip()] = value.strip()

    return result

string = '''{"easy test.txt": {"type": "file", "origin path": "C:\\Users\\zohar\\OneDrive\\Desktop\\Test Cases\\Text\\easy test.txt", "path in archive": "easy test.txt", "pointer": 22, "header length": 20, "encoded size": 2, "unit length": 1, "data hash": "b'}N\\xeb\\xab|\\xe3?,]m\\x8cb@\\xcc\\x8f\\xe6^\\xa1L\\xd7'", "original size": 11}, "easy test2.txt": {"type": "file", "origin path": "C:\\Users\\zohar\\OneDrive\\Desktop\\Test Cases\\Text\\easy test2.txt", "path in archive": "easy test2.txt", "pointer": 46, "header length": 20, "encoded size": 4, "unit length": 1, "data hash": "b'\\x1d\\x904\\xacI\\x13\\x01\\xb53\\x16\\xeb,\\x11\\xb0\\xbfcr\\x83\\xfe\\xc2'", "original size": 19}}'''
result_dict = parse_dict(string)
print(result_dict)


