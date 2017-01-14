import os

from tldextract import tldextract
from urllib import parse, request


class URL:
    __opener = request.build_opener()
    __opener.addheaders = [('User-Agent', 'https://jabbari.io/contact.php')]

    @classmethod
    def get_content_of_url(cls, url : str = None) -> str:
        return cls.__opener.open(url).read()

    @staticmethod
    def validate_url(url: str) -> bool:
        split = parse.urlsplit(url)
        return split.scheme is not '' and split.netloc is not ''

    @staticmethod
    def make_url_from_base(base: str = None, url: str = None) -> str:
        return parse.urljoin(base, url)

    @staticmethod
    def is_same_domain(base: str, url: str, include_sub: bool = True) -> bool:
        if include_sub:
            return tldextract.extract(base).domain == tldextract.extract(url).domain
        else:
            return parse.urlsplit(base).netloc == parse.urlsplit(url).netloc


class IO:
    @staticmethod
    def get_html_cache_dir():
        return "html"

    @staticmethod
    def get_html_cache_with_file(file):
        return os.path.join(IO.get_html_cache_dir(), file)


if __name__ == '__main__':
    # print(URL.validate_url("https://google.com"))
    print(URL.dosomething())
