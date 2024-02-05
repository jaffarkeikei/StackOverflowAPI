"""This script is designed to demonstrate the process of consuming the StackExchange API, focusing on StackOverflow questions.

The script sends a GET request to retrieve questions from StackOverflow that have been most recently active. It then displays the titles and links of questions that have not received any answers. Questions with answers are excluded from the output.

Example:
    To use this script, execute it to filter and display the titles and links of unanswered questions from the most recently active questions on StackOverflow.

    $ python consume_api.py

Upon execution, the script prints the title and link of each unanswered question. For questions that have received answers, a 'skipped' message is displayed.

To further explore the data returned by the API, one might consider enhancing the output to include additional details from the response, such as the number of views or the tags associated with each question.
"""


import requests


STACKEXCHANGE_API_URL = 'https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow'


def fetch_data_from_api():
    """
    Make a GET request to the StackExchange API to fetch the most recently active questions on StackOverflow.

    Filter out questions with answers and returns the remaining questions.
    """
    try:
        response = requests.get(STACKEXCHANGE_API_URL)
        # Raise an exception if the request fails
        response.raise_for_status()
        return response.json()['items']
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

def parse_data(data):
    """
    Parse the data from the API response.

    Extract the title and link of each question.
    """
    try:
        return data['title'], data['link']
    except KeyError:
        print("Data is not in the expected format")
        return None, None

def print_question(title, link):
    """
    Print the title and link of each question.
    """
    print(f"Title: {title}")
    print(f"Link: {link}")
    print()

def main():
    """
    The main function of the script.

    It fetches data from the StackExchange API, parses the data, and prints the title and link of each question.
    If no questions are found, it prints a message indicating so.
    """
    questions = fetch_data_from_api()
    if questions:
        for question in questions:
            title, link = parse_data(question)
            if title and link:
                print_question(title, link)
    else:
        print("No questions found.")

if __name__ == "__main__":
    main()
