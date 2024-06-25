"""
config file for the RLE Compressor software
"""


MAIN_PROMPTS = \
    {"get input": "Please enter the action you would like to perform: ",
     "greeting": "Welcome to the RLE Compressor software.\n",
     "--help": """
Possible actions are:
"c" - to compress
"w" - work on existing archive (extract, show content, add data)
"exit" - to exit the program completely
"--help" - to see this message again

In every mode you will be guided how to proceed.
"""}

MAIN_POSSIBLE_ACTIONS = ["c", "w", "exit", "--help", "info"]

WOA_POSSIBLE_ACTIONS = ["show", "exit", "extract", "whelp", "--help", "add"]

WOA_PROMPTS = \
    {'--whelp': 'Now in archive work mode.\n'
           'Possible actions are:\n'
           '"exit" - to exit the program completely\n'
           '"show" - to show the content of the archive\n'
           '"extract" - to extract data from the archive\n'
           'both actions can take a path in the archive as an argument\n'
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
     Welcome to the Compressor
     First, you will be asked if you want a different unit length for each 
     path, or a default unit length for all paths.
     
     Then, you will be asked to input the path of the directory you want to
     compress. Please input each path separately.
     
     If you chose to have a different unit length for each path, you will be
     asked to input the unit length for each path.""",
        "set default unit length": 'Please enter the default unit length, '
                                   'or press "Enter" to skip: ',
     "another path": "Enter another path or type 'ok' to continue: "}

CI_POSSIBLE_ACTIONS = ["--help", "exit"]
MAX_COUNT = 255
FILE_HEADER_LENGTH = 20
METADATA_HEADER_LENGTH = 4
METADATA_FOOTER_LENGTH = 4

