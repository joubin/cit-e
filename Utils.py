import os, hashlib

from tldextract import tldextract
from urllib import parse, request


class URL:
    __opener = request.build_opener()
    __opener.addheaders = [('User-Agent', 'https://jabbari.io/contact.php')]

    @classmethod
    def get_content_of_url(cls, url: str = None) -> str:
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

    @staticmethod
    def url_to_file(url: str = None) -> str:
        return IO.url_to_file(url)

    @classmethod
    def get_useragent(cls):
        return cls.__opener.addheaders[0][1]


class IO:
    read_cache = True
    path = "html"
    hashlib = hashlib.sha256

    @classmethod
    def get_html_cache_dir(cls):
        if not os.path.exists(cls.path):
            os.mkdir(cls.path)
        return cls.path

    @staticmethod
    def get_html_cache_with_file(file):
        return os.path.join(IO.get_html_cache_dir(), file)

    @staticmethod
    def url_to_file(url: str = None) -> str:
        return url.replace("https://", "https-").replace("http://", "http-").replace('/', '<>')

    @staticmethod
    def cached_file_exists(url: str = None) -> bool:
        return os.path.exists(IO.get_html_cache_with_file(url))

    @staticmethod
    def hash_file_name(filename: str = None) -> str:
        return hashlib.sha256(filename.encode("UTF-8")).hexdigest()

