import os
class UI:
        @staticmethod
        def get_response(possible_responses, prompt="what to do next? "):
            """
            Get user input. make sure the input is something we can work with.

            """
            while True:
                user_input = zinput()
                if user_input.lower() in possible_responses.keys():
                        return user_input

                print("Invalid input. Please try again")
