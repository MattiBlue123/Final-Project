from helper_functions import zinput
from work_on_archive import WorkOnArchive
from compression_init import CompressorInit
from config import *

class Main:
    """
    This class is the main class of the program. It runs the main decision tree
    """
    def main_decision_tree(self, user_input):
        """
        :param user_input:
        "c" - to compress
        "w" - to work on an existing archive (extract, add, show)
        "info" - to get info about an archive
        "--help" - to see this message again
        "exit" - to exit the program completely
        :return:
        """
        if user_input == 'c':
            c = CompressorInit()
            c.compressor_init_main()
        elif user_input == 'w':
            w = WorkOnArchive()
            w.work_on_archive_main()


    @staticmethod
    def get_user_input():
        """
        This function gets the user input and validates it
        :return:
        """
        while True:
            response = zinput(MAIN_PROMPTS["get input"])
            if len(response) == 0 or len(response) > 1:
                print("Invalid response1")
                continue
            if response not in MAIN_POSSIBLE_ACTIONS:
                continue
            if response == '--help':
                print(MAIN_PROMPTS["--help"])
                continue
            return response

    def main(self):
        while True:
            # say hello to user, explain rules
            print(MAIN_PROMPTS["greeting"])
            print(MAIN_PROMPTS["--help"])
            # get user input
            response = self.get_user_input()
            # run main decision tree
            self.main_decision_tree(response)



if __name__ == '__main__':
    Main().main()


