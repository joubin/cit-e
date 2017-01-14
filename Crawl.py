from ssl import CertificateError
from urllib import parse, request, error

import tldextract

from Page import Page


class Crawl:
    def __init__(self, base_domain: str = None):
        self.__base_domain = base_domain
        self.__urls = dict()

    def get_base_domain(self):
        return self.__base_domain

    def crawl(self, url: str = None):
        print("Going in")
        if url is None:
            url = self.__base_domain
        if url is "#" or self.is_x_in_y(url) or url.endswith(".pdf"):
            return
        print("Url", url)
        page = Page(url)
        self.set_done_scanning(url)
        print(len(page.get_links()))
        for link in page.get_links():
            print("-->", link)
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
    import sys, time

    start = time.time()
    sys.setrecursionlimit(sys.getrecursionlimit() * 2)
    crawl = Crawl("http://jabbari.io")
    crawl.crawl()
    end = time.time()
    print(crawl.get_url_count())
    print("Took ", (end - start), " seconds")
    # page = Page("https://jabbari.io/blog.php")
    # print(page.get_links())
    # crawl.print_urls()
