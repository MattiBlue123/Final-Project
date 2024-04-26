

DI_POSSIBLE_ACTIONS = ['show', "exit", "extract", "d help"]

DI_PROMPTS = \
    {"d help": "welcome to the decompressor.\n"
                  "At any time, you can type 'exit' to quit.\n"
                  "First you need to input the path of the archive file\n"
                  "then type 'show' the content directory of the "
                  "archive.\n"
                  "show: If you want to show a specific directory in the archive\n"
                  "you can type 'show' followed by the directory path\n"
                  "in the following format: 'show /path/to/directory'.\n"
                  "extract: You can type 'extract' followed by the directory path\n"
                  "in the following format: 'extract /path/to/directory'\n"
                  "If you need help type 'd help' to see this message again.",
     "get input": "Please enter the action you would like to perform: "}
print(DI_PROMPTS["help"])