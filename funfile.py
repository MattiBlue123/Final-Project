string = '{"folder": {"type": "folder", "1313.png": {"type": "file", "pointer": 151928, "encoded size": 151908, "unit length": 1, "original size": 80358}, "folder_rle_compressed.bin": {"type": "file", "pointer": 360122, "encoded size": 208174, "unit length": 1, "original size": 108351}, "INFI - HW 11-1.pdf": {"type": "file", "pointer": 716516, "encoded size": 356374, "unit length": 1, "original size": 179457}, "New folder": {"type": "folder", "something else": {"type": "folder", "ddddd.txt": {"type": "file", "pointer": 716588, "encoded size": 52, "unit length": 1, "original size": 26}}, "Somthing": {"type": "folder"}, "stuff.docx": {"type": "file", "pointer": 736386, "encoded size": 19778, "unit length": 1, "original size": 11994}}, "testty.txt": {"type": "file", "pointer": 736476, "encoded size": 70, "unit length": 1, "original size": 57}, "zipped_rle_compressed.bin": {"type": "file", "pointer": 749694, "encoded size": 13198, "unit length": 1, "original size": 6656}}}'
string = string.encode('utf-8')
string = string.decode('utf-8')
dict = eval(string)
print(dict)
print(type(dict))

