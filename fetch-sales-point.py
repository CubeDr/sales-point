import requests
from bs4 import BeautifulSoup
import re
import github
from datetime import datetime
import os


def to_int(text):
  return int(text.replace(',', ''))


def fetch_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        return f'Error fetching data: {e}'


def fetch(url):
    element = fetch_soup(url).select_one('.gd_sellNum')

    if element:
        text = element.text.strip()
        number_part = re.search(r'\d{1,3}(?:,\d{3})*', text)  # Find one or more digits

        if number_part:
            return to_int(number_part.group())
        else:
            return 'Number not found within the text'
    else:
        return 'Element with class "gd_sellNum" not found'


def append(score):
    # Authentication
    github_token = os.getenv('ACCESS_TOKEN')
    print('access token length: ' + str(len(github_token))
    g = github.Github(github_token)

    repo = g.get_repo('CubeDr/sales-point')

    contents = repo.get_contents('yes24.csv')
    repo.update_file(contents.path, 'Test commit', f'{score}, {datetime.now()}\n{contents.decoded_content.decode()}', contents.sha)

    g.close()


if __name__ == '__main__':
    score = fetch('https://www.yes24.com/Product/Goods/117372853')
    append(score)

