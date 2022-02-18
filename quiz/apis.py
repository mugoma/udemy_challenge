"""Script contianing the api that retrieves the quiz questions
"""
import requests


def fetch_quiz_api(fetch_url):
    """Fetch the question lists from the url provided.


    Response/Output format:
    -----------------------


    {   

        title:`str`,\n
        questions:
            [
                {
                    "question_text": "`str/int`",
                    "choices": {
                        "1": "str/int"
                    },
                    "answer": "str/int",

                    //Optional arguments

                    "multi_answer":"bool",//Default False
                    "randomize_choices":"bool"//Default False

                }
                ...
            ],

    }
    """
    response = requests.get(fetch_url)
    return response.json()
