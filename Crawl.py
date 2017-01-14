from ssl import CertificateError
from urllib import parse, request, error

import tldextract
from bs4 import BeautifulSoup, SoupStrainer

from Utils import URL as URL_UTIL


class Crawl:
    def __init__(self, base_domain: str = None):
        self.__base_domain = base_domain
        self.__urls = dict()
        self.__opener = request.build_opener()
        self.__opener.addheaders = [('User-Agent', 'https://jabbari.io/contact.php')]

    def get_base_domain(self):
        return self.__base_domain

    def crawl(self, url: str = None):
        if url is None:
            url = self.__base_domain
        if url is "#" or self.is_x_in_y(url) or url.endswith(".pdf"):
            return
        try:

            html = self.__opener.open(url).read()
            soup = BeautifulSoup(html, "lxml", parse_only=SoupStrainer('a', href=True))
            for link in soup.find_all('a'):
                tmp_link = link['href']
                if not URL_UTIL.validate_url(tmp_link) and tmp_link != "#":
                    tmp_link = URL_UTIL.make_url_from_base(url, tmp_link)
                if URL_UTIL.validate_url(tmp_link) and self.is_same_domain(tmp_link):
                    self.add_new_url(tmp_link)
                    self.set_done_scanning(url)
                    self.crawl(tmp_link)
        except error.HTTPError:
            pass
        except TimeoutError:
            pass
        except CertificateError:
            pass
        except error.URLError:
            pass
        except Exception:
            pass

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
    crawl = Crawl("http://uber.com")
    crawl.crawl()
    end = time.time()
    print(crawl.get_url_count())
    print("Took ", (end - start), " seconds")

    # crawl.print_urls()
