import string
import os
import requests
from bs4 import BeautifulSoup


# def url_input():
#     print('Input the URL:')
#     url = input()
#     return url
#
#
# def url_response(url):
#     response = requests.get(url)
#     if response.status_code != 200:
#         print(f'The URL returned {response.status_code}!')
#         return False
#     return True
#
#
# def url_response_movie(url):
#     response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
#     if response.status_code != 200 or 'imdb' not in url or 'title' not in url:
#         print('Invalid movie page!')
#         return None
#     soup = BeautifulSoup(response.content, 'html.parser')
#     response_list = list([soup.find('h1').text])
#     response_list.append(soup.find('span', {'data-testid': 'plot-l'}).text)
#     return response_list
#
#
# def dict_constructor(response):
#     result = dict()
#     result['title'] = response[0]
#     result['description'] = response[1]
#     return result
#
#
# def saving_to_html_file(url):
#     if url_response(url):
#         with open('source.html', 'wb') as file:
#             file.write(requests.get(url).content)
#             print('Content saved.')
#             file.close()


def look_for_article_nature(url, art_type):
    result = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    result_of_seeking = soup.find_all('article')
    for art in result_of_seeking:
        type_of_art = art.find('span', {'class': 'c-meta__type'}).text
        if type_of_art == art_type:
            href = 'https://www.nature.com' + art.find('a').get('href')
            result.append(href)
    return result


def extract_only_text(url):
    space_table = str.maketrans({' ': '_'})
    no_punc_table = str.maketrans(dict.fromkeys(string.punctuation))
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title').text
    title = title.translate(no_punc_table)
    title = title.translate(space_table)
    article_text = soup.find('div', {'class': 'c-article-body u-clearfix'}).text.strip().encode("UTF-8")
    with open(f'{title}.txt', 'wb') as file:
        file.write(article_text)
        file.close()


def folder_creation(num):
    folder = f'Page_{num}'
    if os.access(folder, os.F_OK):
        os.chdir(folder)
        for file in os.listdir():
            os.remove(file)
        os.chdir('..')
        os.rmdir(folder)
    os.mkdir(folder)
    os.chdir(folder)


def collecting_of_articles(year, page, article_type):
    url = f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year={year}&page={page}'
    links = look_for_article_nature(url, article_type)
    for link in links:
        extract_only_text(link)


def main():
    #  url = url_input()
    # response = url_response_movie(url)
    # if response:
    #     print(dict_constructor(response))
    # saving_to_html_file(url)
    print("Enter the year:")
    year = int(input())
    print("Enter the number of the last page:")
    page_num = int(input())
    print('Enter the type of articles you want to save:')
    article_type = input()
    os.mkdir(f'{article_type} of {year}')
    os.chdir(f'{article_type} of {year}')
    for page in range(1, page_num + 1):
        folder_creation(page)
        collecting_of_articles(year, page, article_type)
        os.chdir('..')
    os.chdir('..')
    print('All articles are saved.')


if __name__ == '__main__':
    main()
