from typing import List, Dict
from bs4 import BeautifulSoup

from Utils import URL as URL_UTIL, IO as IO_UTIL


class Page:

    def __init__(self, url: str = None):
        self.url = url
        self.response = bytes()
        self.__soup = None
        self.__load_page(url)
        self.__soup = BeautifulSoup(self.response, "lxml")

        self.links = list()
        self.__get_links()

        self.__forms = list()
        self.__get_forms()

        self.__inputs = list()
        self.__get_inputs()

        self.__write_to_file()

    def __load_page(self, url: str, load_cache: bool = IO_UTIL.read_cache) -> str:
        if load_cache:
            print("loading cache")
            try:
                with open(IO_UTIL.get_html_cache_with_file(IO_UTIL.hash_file_name(url)), 'rb') as file:
                    self.response = file.read()
            except FileNotFoundError:
                return self.__load_page(url, load_cache=False)
            except OSError:
                return self.__load_page(url, load_cache=False)
        else:
            try:
                self.response = URL_UTIL.get_content_of_url(url)
            except Exception as error:
                print(error, url, "load_cache", IO_UTIL.read_cache)

    def __get_links(self):
        self.links = list()
        for link in self.__soup.find_all('a'):

            if link is not None and link.has_attr('href'):
                tmp_link = link['href']
                if not URL_UTIL.validate_url(tmp_link) and tmp_link != "#":
                    tmp_link = URL_UTIL.make_url_from_base(self.url, tmp_link)
                if URL_UTIL.validate_url(tmp_link) and URL_UTIL.is_same_domain(self.url, tmp_link):
                    self.links.append(tmp_link)

    def __get_forms(self):
        print("getting called")
        self.__forms = list()

        for form in self.__soup.find_all('form'):
            try:
                self.__forms.append((form['method'], form["action"]))
            except KeyError as e:
                print("Keyerror", e)
        return self.__forms

    def __get_inputs(self):
        self.__inputs = list()
        for this_input in self.__soup.find_all('input'):
            self.__inputs.append(this_input)

    def get_forms(self) -> List:
        return self.__forms

    def get_links(self) -> List:
        return self.links

    def has_forms(self) -> bool:

        return len(self.__forms) > 0

    def get_inputs(self):
        return self.__inputs

    def has_links(self) -> bool:
        return len(self.links) > 0

    def has_input(self) -> bool:
        return len(self.get_inputs()) > 0

    def get_response(self, pretty: bool = False):
        if pretty:
            return self.__soup.prettify()
        else:
            return self.response

    def __write_to_file(self):
        if not IO_UTIL.cached_file_exists(self.url):
            with open(IO_UTIL.get_html_cache_with_file(
                    IO_UTIL.hash_file_name(self.url)),
                    mode='w+') as file:
                file.write(self.get_response(pretty=True))

    def get_child_url(self, url:str)->str:
        URL_UTIL.make_url_from_base(self.url, url)


if __name__ == '__main__':
    page = Page("https://jabbari.io/contact.php")
    print(page.get_forms())
    print(page.get_response(pretty=True))
