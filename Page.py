from bs4 import BeautifulSoup, SoupStrainer
from Utils import URL as URL_UTIL, IO as IO_UTIL


class Page:
    def __init__(self, url: str = None):
        self.url = url
        self.__soup = BeautifulSoup(URL_UTIL.get_content_of_url(url), "lxml", parse_only=SoupStrainer('a', href=True))
        self.links = list()
        self.__get_links()

    def __get_links(self):
        self.links = list()
        for link in self.__soup.find_all('a'):
            tmp_link = link['href']
            if not URL_UTIL.validate_url(tmp_link) and tmp_link != "#":
                tmp_link = URL_UTIL.make_url_from_base(self.url, tmp_link)
            if URL_UTIL.validate_url(tmp_link) and URL_UTIL.is_same_domain(self.url, tmp_link):
                self.links.append(tmp_link)

    def __write_to_file(self):
        with open(IO_UTIL.get_html_cache_with_file(self.url), mode='w+') as file:
            file.write(self.__soup)

