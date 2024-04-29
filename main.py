from helper_functions import zinput
from decompression_init import DecompressorInit
from compression_init import CompressorInit
from config import *


class Main:

    def main_decision_tree(self, user_input):
        """
        :param user_input:
        "c" - to compress
        "d" - to extract (decompress)
        "info" - to get info about an archive
        "--help" - to see this message again
        "back" - to go back to the main menu
        "exit" - to exit the program completely
        :return:
        """
        if user_input == 'c':
            c = CompressorInit()
            c.compressor_init_main()
        elif user_input == 'd':
            d = DecompressorInit()
            d.decompressor_init_main()


    @staticmethod
    def get_user_input():
        while True:
            response = zinput(MAIN_PROMPTS["get input"]).lower().strip()
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
            response = self.get_user_input()
            self.main_decision_tree(response)



if __name__ == '__main__':
    Main().main()


