"""
This script is designed to interact with the StackExchange API.

It retrieves and displays a list of the top 'k' most viewed questions on StackOverflow within a user-defined date range. The script allows users to specify the start and end dates of the range, as well as the minimum number of views a question must have to be included in the list. This functionality is particularly useful for identifying popular topics or issues within a specific timeframe, providing insights into what the StackOverflow community is most interested in or struggling with during that period.
"""

import sys
import requests


STACKEXCHANGE_API_URL = 'https://api.stackexchange.com/2.3/search/advanced'


def fetch_top_k_viewed_questions(from_date, to_date, min_views):
    """
    Fetches and returns a list of the top k most viewed StackOverflow questions within a specified date range.

    Parameters:
    - from_date (str): The start date of the range, formatted as 'YYYY-MM-DD'.
    - to_date (str): The end date of the range, also formatted as 'YYYY-MM-DD'.
    - min_views (int): The number of top-viewed questions to retrieve.

    Returns:
    - A list of dictionaries, where each dictionary represents one of the top k viewed questions. Each dictionary contains details such as the question's title, view count, and URL.
    """
    API_URL = STACKEXCHANGE_API_URL
    params = {
        "order": "desc",
        "sort": "creation",
        "site": "stackoverflow",
        "fromdate": from_date,
        "todate": to_date,
        "min": min_views,
        "pagesize": min_views,
    }
    response = requests.get(API_URL, params=params)
    questions = response.json().get("items", [])

    # Sorting questions by view count in descending order
    sorted_questions = sorted(questions, key=lambda x: x['view_count'], reverse=True)
    return sorted_questions

def main():
    """
    The main function of the script.

    It first checks if the correct number of command-line arguments are provided. If not, it prints a usage message and exits. If the correct number of arguments are provided, it proceeds to fetch the top k most viewed StackOverflow questions within the specified date range.
    It then prints the title, view count, and link of each question in an orderly manner.

    Example usage from the command line:
        python most_viewed_questions.py 2021-01-01 2021-01-31 10
    This will fetch and display the top 10 most viewed questions on StackOverflow from January 1, 2021, to January 31, 2021.

    Parameters:
    - None, but expects three command-line arguments in the following order:
        1. from_date (str): The start date of the range, formatted as 'YYYY-MM-DD'.
        2. to_date (str): The end date of the range, also formatted as 'YYYY-MM-DD'.
        3. number_of_questions (int): The number of top-viewed questions to retrieve.

    Returns:
    - None. The function prints the fetched questions to the standard output in an orderly manner.
    """
    # Check for the correct number of arguments
    if len(sys.argv) != 4:
        print("Usage: python most_viewed_questions.py <from_date> <to_date> <number_of_questions>")
        sys.exit(1)

    from_date, to_date, number_of_questions = sys.argv[1], sys.argv[2], int(sys.argv[3])

    top_questions = fetch_top_k_viewed_questions(from_date, to_date, number_of_questions)

    # Print the questions with links
    for i, question in enumerate(top_questions, start=1):
        print(f"{i}. {question['title']}\n   Views: {question['view_count']}\n   Link: {question['link']}\n")

if __name__ == "__main__":
    main()
