"""
config file for the RLE Compressor software
"""

MAIN_PROMPTS = \
    {"get input": "Please enter the action you would like to perform: ",
     "greeting": "\n\033[1mWelcome to the RLE Compressor software.\033[0m\n",
     "--help": """
Possible actions are:
"c" - to compress
    while compressing:
        1. insert the path to the file or directory you want to
        compress
        2. insert the unit length - optional for setting default.

"w" - to work on an existing archive (extract, add, show)
    while working on an archive:
        1. insert the path to the archive
        2. choose what to do with the archive

"--help" - to see this message again
"exit" - to exit the program completely

In every mode you will be guided how to proceed.
"""}

MAIN_POSSIBLE_ACTIONS = ["c", "w", "exit", "--help", "info"]

WOA_POSSIBLE_ACTIONS = ["show", "exit", "extract", "whelp", "--help", "add"]

WOA_PROMPTS = \
    {'--whelp': '\n\033[1mNow in archive work mode.\033[0m\n'
                'First, you will be asked to enter the path to the archive.\n'
                'Possible actions are:\n'
                '"exit" - to exit the program completely\n'
                '"add" - to add data to the archive\n'
                '"show" - to show the content of the archive\n'
                '"extract" - to extract data from the archive\n'
                'actions can take a path in the archive as an argument\n'
                'path format: /dir1/dir2/file\n'
                '"whelp" - to see this message again.'
                '"--help" - to see the main manu again (exit to open software in '
                'c mode)\n',
     'get input': "What would you like to do with the archive? "}
FLAGS = {"back_flag": False, "exit_flag": False}

CI_PROMPTS = \
    {"get input": "Please enter the action you would like to perform: ",
     "get ul": "Please enter the unit length: ",
     "get path": "Please enter the path of the data you want to compress: ",
     "chelp": """
     \n\033[1mNow in Compressing mode.\033[0m\n
     1. Set default unit length or skip.
     2. Enter the directory you want to compress.
     3. Enter the unit length for the directory (if default is not set).
     4. Repeat steps 2 and 3 for additional directories.     """,
     "set default unit length": 'Enter the default unit length ("Enter" to '
                                'skip): ',
     "another path": "Enter another path or type 'ok' to continue: "}

CI_POSSIBLE_ACTIONS = ["--help", "exit"]
MAX_COUNT = 255
FILE_HEADER_LENGTH = 20
METADATA_HEADER_LENGTH = 4
METADATA_FOOTER_LENGTH = 4
METADATA_HEADER = b'ZM\x01\x02'
METADATA_FOOTER = b'ZM\x05\x06'
