MAIN_PROMPTS = \
    {"get input": "Please enter the action you would like to perform: ",
     "greeting": "Welcome to the ZoZ RLE Compressor software.\n"
                 "Using this software,you can compress or extract files,\n "
                 "get info about compressed files and add files to the "
                 "archive.\n",
     "--help": """
Possible actions are:
"c" - to compress
"d" - to extract (decompress)
"info" - to get info about an archive
"exit" - to exit the program completely
"back" - to go back to the main menu
"--help" - to see this message again
"""}

MAIN_POSSIBLE_ACTIONS = ["c", "d", "exit", "--help", "info", "back"]


DI_POSSIBLE_ACTIONS = ["show", "exit", "extract", "dhelp", "back", "--help"]

DI_PROMPTS = \
    {"dhelp": "welcome to the decompressor.\n"
              "At any time, you can type 'exit' to quit.\n"
              "First you need to input the path of the archive file\n"
              "then type 'show' the content directory of the "
              "archive.\n"
              "show: If you want to show a specific directory in the archive\n"
              "you can type 'show' followed by the directory path\n"
              "in the following format: 'show /path/to/directory'.\n"
              "extract: You can type 'extract' followed by the directory path\n"
              "in the following format: 'extract /path/to/directory'\n"
              "If you need help type 'dhelp' to see this message again.",
     "get input": "Please enter the action you would like to perform: "}

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