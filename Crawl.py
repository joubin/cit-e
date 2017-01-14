from urllib import parse, robotparser
import tldextract
import sys, time
from Page import Page
from Utils import URL as URL_URLS


class Crawl:
    obey_robot = True

    def __init__(self, base_domain: str = None):
        self.__base_domain = base_domain
        self.__urls = dict()
        self.__rp = robotparser.RobotFileParser()
        self.__rp.set_url(base_domain + "/robots.txt")
        self.__rp.read()
        self.__delay = self.__rp.crawl_delay(URL_URLS.get_useragent())
        if self.__delay is None:
            self.__delay = float(0)
        else:
            self.__delay = float(self.__delay)

        print(self.__delay)

    def get_base_domain(self):
        return self.__base_domain

    def crawl(self, url: str = None):
        time.sleep(self.__delay)
        if url is None:
            url = self.__base_domain
        if url is "#" or self.is_x_in_y(url) or url.endswith(".pdf"):
            return
        if Crawl.obey_robot:
            if not self.__rp.can_fetch("*", url):
                return

        page = Page(url)
        self.set_done_scanning(url)
        for link in page.get_links():
            self.add_new_url(link)
            self.crawl(link)

    def is_same_domain(self, url: str, include_sub: bool = True) -> bool:
        if include_sub:
            return tldextract.extract(self.__base_domain).domain == tldextract.extract(url).domain
        else:
            return parse.urlsplit(self.__base_domain).netloc == parse.urlsplit(url).netloc

    def add_new_url(self, url: str = None) -> None:
        if url not in self.__urls.keys():
            self.__urls[url] = False

    def set_done_scanning(self, url: str = None):
        self.__urls[url] = True

    def print_urls(self):
        for url in self.__urls:
            print(url)

    def is_x_in_y(self, url):
        if url not in self.__urls.keys():
            self.add_new_url(url)
        return self.__urls[url]

    def get_url_count(self) -> int:
        return len(self.__urls)


if __name__ == '__main__':

    start = time.time()
    sys.setrecursionlimit(sys.getrecursionlimit() * 2)
    crawl = Crawl("https://uber.com")
    crawl.crawl()
    end = time.time()
    print(crawl.get_url_count())
    print("Took ", (end - start), " seconds")
