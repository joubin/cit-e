from typing import List

from bs4 import BeautifulSoup, SoupStrainer
from Utils import URL as URL_UTIL, IO as IO_UTIL


class Page:
    def __init__(self, url: str = None):
        self.url = url
        self.response = bytes()
        self.__soup = None
        self.__load_page(url)
        self.__soup = BeautifulSoup(self.response, "lxml", parse_only=SoupStrainer('a', href=True))

        self.links = list()
        self.__get_links()
        if IO_UTIL.write_to_file():
            self.__write_to_file()

    def __load_page(self, url: str, load_cache: bool = IO_UTIL.read_cache) -> str:
        if load_cache:
            try:
                with open(IO_UTIL.get_html_cache_with_file(IO_UTIL.url_to_file(url)), 'rb') as file:
                    self.response = file.read()
            except FileNotFoundError:
                return self.__load_page(url, load_cache=False)
        else:
            try:
                self.response = URL_UTIL.get_content_of_url(url)
            except Exception as error:
                print(error, url, "load_cache", IO_UTIL.read_cache)

    def __get_links(self):
        self.links = list()
        for link in self.__soup.find_all('a'):
            tmp_link = link['href']
            if not URL_UTIL.validate_url(tmp_link) and tmp_link != "#":
                tmp_link = URL_UTIL.make_url_from_base(self.url, tmp_link)
            if URL_UTIL.validate_url(tmp_link) and URL_UTIL.is_same_domain(self.url, tmp_link):
                self.links.append(tmp_link)

    def get_links(self) -> List:
        return self.links

    def __write_to_file(self):
        if not IO_UTIL.cached_file_exists(self.url):
            with open(IO_UTIL.get_html_cache_with_file(
                    self.url.replace("https://", "https-").replace("http://", "http-").replace('/', '<>')),
                    mode='wb') as file:
                file.write(self.response)
