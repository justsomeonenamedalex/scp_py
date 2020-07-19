# Main article thing

import requests
from bs4 import BeautifulSoup
import re

import exceptions


class Article:
    """Base class for main-list wiki articles"""

    def __init__(self, article_number: str = None, soup: BeautifulSoup = None, link: str = None):

        self.url = None  # Link to article
        if link:
            self.url = link
        self.soup = None  # BeautifulSoup object of the page
        self.title = None  # Title of the article
        self.plaintext = None  # Text without newline characters
        self.text = None  # Text with newline characters
        self.item_label = None  # Label of item, eg: SCP-173
        self.item_number = None  # Number of item, eg: 173
        if article_number:
            self.item_number = article_number
        self.object_class = None  # Object class of item, eg: Euclid
        self.special_containment_procedures = None  # Special containment procedures of the object
        self.short_description = None  # Short description of the object
        self.images = None  # Images in the article
        self.collapsible_blocks = None
        self.rating = None  # Rating of the page
        self.page_tags = None  # What the page is tagged with

        if article_number:
            self.get_page_from_number(article_number)
        elif soup:
            self.get_page_from_soup(soup)
        elif link:
            self.get_page_from_link(link)

    def __str__(self):
        return self.text

    def get_page_from_number(self, number: str):
        """Create the article from a scp number"""
        base_url = "http://www.scp-wiki.net/scp-"
        if len(number) < 3:
            number = "0"*(3-len(number)) + number
        url = base_url + number
        self.get_page_from_link(url)

    def get_page_from_link(self, link: str):
        """Create the article from a link to the page"""

        if link == "http://www.scp-wiki.net/scp-001":
            raise exceptions.SCP001ERROR

        response = requests.get(link)

        if not ("scp-wiki.net" in link):
            raise exceptions.NOTSCPWIKILINK(link)

        if not ("/scp-" in link):
            raise exceptions.NOTMAINLISTSCP(link)

        soup = BeautifulSoup(response.text, "html.parser")
        self.get_page_from_soup(soup)

    def get_page_from_soup(self, soup: BeautifulSoup):
        """Create the article from a BeautifulSoup object"""
        self.soup = soup
        self.format_soup(soup)

    def format_soup(self, soup: BeautifulSoup):
        page_content = soup.find(id="page-content")
        if not page_content:
            raise exceptions.CONTENTNOTFOUND

        # Make sure the page has been created
        warning_sign = page_content.find("h1", id="toc0")
        if warning_sign:
            if warning_sign.text == "This page doesn't exist yet!":
                print(page_content.find(id="toc0").text)
                raise exceptions.PAGENOTCREATED

        paragraphs = page_content.find_all(["p", "ul", "ol", "strong"], recursive=False)

        paragraph_texts = [i.text for i in paragraphs]
        main_text = "\n".join(paragraph_texts)

        try:
            if not (paragraph_texts[0].startswith("Item #: ")):
                self.title = paragraph_texts[0]
        except IndexError:
            print("Failed to load title")
        except Exception as e:
            raise exceptions.CONTENTNOTFOUND("Title", e)

        self.text = main_text

        self.plaintext = " ".join(paragraph_texts)

        try:
            self.item_label = re.search(r"Item #: (.*?)\n", main_text).group(1)
        except AttributeError:
            print("Failed to load item_label")
        except Exception as e:
            raise exceptions.CONTENTNOTFOUND("item_label", e)

        try:
            self.item_number = re.search(r"Item #: SCP-(.*?)\n", main_text).group(1)
        except AttributeError:
            print("Failed to load item_number")
        except Exception as e:
            raise exceptions.CONTENTNOTFOUND("item_number", e)

        try:
            self.object_class = re.search(r"Object Class: (.*?)\n", main_text).group(1)
        except AttributeError:
            print("Failed to load object_class")
        except Exception as e:
            raise exceptions.CONTENTNOTFOUND("object_class", e)

        try:
            self.url = "http://www.scp-wiki.net/scp-"+self.item_number
        except TypeError:
            print("Failed to save url")
        except Exception as e:
            raise exceptions.CONTENTNOTFOUND("url", e)

        try:
            self.special_containment_procedures = "Special Containment Procedures:" + re.search(r"Special Containment Procedures:(.*?)\nDescription:", main_text, re.DOTALL).group(1)
        except AttributeError:
            print("Failed to load special_containment_procedures")
        except Exception as e:
            raise exceptions.CONTENTNOTFOUND("special_containment_procedures", e)

        try:
            self.short_description = "Description: " + re.search(r"Description: (.*?)\n", main_text).group(1)
        except AttributeError:
            print("Failed to load short_description")
        except Exception as e:
            raise exceptions.CONTENTNOTFOUND("short_description", e)

        try:
            self.images = [[image.find("img")["src"], image.find("p").text] for image in page_content.find_all(class_="scp-image-block")]
        except KeyError:
            print("Failed to load images")
        except Exception as e:
            raise exceptions.CONTENTNOTFOUND("images", e)

        try:
            self.collapsible_blocks = [[block.find(class_="collapsible-block-folded").find("a").text, "\n".join([i.text for i in block.find(class_="collapsible-block-content").find_all("p")])] for block in page_content.find_all(class_="collapsible-block")]
        except AttributeError:
            print("Failed to load collapsible_blocks")
        except Exception as e:
            raise exceptions.CONTENTNOTFOUND("collapsible_blocks", e)

        try:
            self.rating = soup.find(class_="rate-points").find(class_="number").text
        except AttributeError:
            print("Failed to load rating")
        except Exception as e:
            raise exceptions.CONTENTNOTFOUND("rating", e)

        try:
            self.page_tags = [i.text for i in soup.find(class_="page-tags").find_all("a")]
        except AttributeError:
            print("Failed to load page_tags")
        except Exception as e:
            raise exceptions.CONTENTNOTFOUND("page_tags", e)
