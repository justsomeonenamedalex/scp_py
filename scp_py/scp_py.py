"""Main module."""
from article import Article
import exceptions
import random


def random_article() -> Article:
    number = str(random.randint(2, 6000))
    try:
        page = Article(article_number=number)
        return page
    except exceptions.PAGENOTCREATED:
        return random_article()


def get_article(number: str) -> Article:
    number = str(number)
    return Article(article_number=number)


def get_article_from_link(link: str) -> Article:
    return Article(link=link)
