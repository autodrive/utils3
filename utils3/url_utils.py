import bs4
import requests


def select_all_links_from_url(url):
    """
    :param url: a given address
    :return:
    """
    return select_all_tags_from_url(url, 'a')


def select_all_tags_from_url(url, tag):
    """
    :param url: a given address
    :param tag: a tag to select
    :return:
    """
    soup = boil_soup(url)
    # select all links
    selected = soup.select(tag)
    # return the links found
    return selected


def boil_soup(book_url):
    # get text from the url
    # http://hwanho.net/blog/2014/12/03/python-bs4/
    source_code = requests.get(book_url)
    plain_text = source_code.text
    # run bs4 parser
    soup = bs4.BeautifulSoup(plain_text, 'lxml')
    return soup
