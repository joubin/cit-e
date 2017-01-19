from urllib import parse, robotparser
import tldextract
import sys, time, sqlite3, os, hashlib
from  sqlite3 import IntegrityError

from Page import Page
from Utils import URL as URL_URLS
from Utils import IO as IOUTILS


class Crawl:
    obey_robot = True

    def __init__(self, base_domain: str = None):
        self.__base_domain = base_domain
        self.__urls = dict()
        self.__rp = robotparser.RobotFileParser()
        self.__rp.set_url(base_domain + "/robots.txt")
        self.__rp.read()
        self.__delay = 0
        try:
            self.__delay = self.__rp.crawl_delay(URL_URLS.get_useragent())
        except:
            pass
        self.pages = list()
        if self.__delay is None:
            self.__delay = float(0)
        else:
            self.__delay = float(self.__delay)

        db = IOUTILS.hash_file_name(base_domain + ".db")

        if not os.path.exists(db):
            file = open(db, "w+")
            file.close()
        try:
            self.__conn = sqlite3.connect(db)
            self.__conn.execute(
                '''CREATE TABLE pages
                (id integer primary key, url string UNIQUE, path, has_forms BOOL, has_links bool)''')
            self.__conn.execute('''CREATE TABLE forms (id integer primary key, pageid integer, method, action)''')
            self.__conn.execute('''CREATE TABLE links (id integer primary key, pageid, parentid)''')
        except Exception:
            pass
        print("going")

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
        self.add_new_page(page)
        self.record_forms(page)
        self.set_done_scanning(url)
        for link in page.get_links():
            self.add_new_url(link, page.url)
            self.crawl(link)

    def is_same_domain(self, url: str, include_sub: bool = True) -> bool:
        if include_sub:
            return tldextract.extract(self.__base_domain).domain == tldextract.extract(url).domain
        else:
            return parse.urlsplit(self.__base_domain).netloc == parse.urlsplit(url).netloc

    def add_new_page(self, page: Page) -> None:
        try:
            with self.__conn as con:
                con.execute('insert into pages(url, path, has_forms, has_links) values (?, ?, ?, ?)',
                            (page.url, IOUTILS.get_html_cache_with_file(IOUTILS.hash_file_name(page.url)),
                             page.has_forms(), page.has_links()))
        except IntegrityError as e:
            pass

    def add_new_url(self, url: str = None, reference: str = None) -> None:
        parentid = self.__conn.execute('select * from pages where url=?', (reference,)).fetchone()[0]
        try:
            selfid = self.__conn.execute('select * from pages where url=?', (url,)).fetchone()[0]
        except TypeError:
            return
        with self.__conn as con:
            con.execute('insert into links(pageid, parentid) values (?, ?)', (selfid, parentid,))

    def set_done_scanning(self, url: str = None):
        self.__urls[url] = True

    def print_urls(self):
        for url in self.__urls:
            print(url)

    def is_x_in_y(self, url) -> bool:
        with self.__conn as con:
            row = con.execute("select * from pages where url=?", (url,)).fetchall()
        return len(row) > 0

    def get_url_count(self) -> int:
        return len(self.__urls)

    def record_forms(self, page: Page):
        for form in page.get_forms():
            with self.__conn as con:
                id = con.execute("select id from pages where url=?", (page.url,)).fetchone()
                con.execute("insert into forms(pageid, method, action) values(?, ?, ?)", (id[0], form[0], form[1],))


if __name__ == '__main__':
    start = time.time()
    sys.setrecursionlimit(sys.getrecursionlimit() * 2)
    # crawl = Crawl("https://uber.com")
    crawl = Crawl("https://jabbari.io")
    crawl.crawl()
    # for page in crawl.pages:
    #     if page.has_forms():
    #         print(page.url, "has", len(page.get_forms()), "form(s)")
    #     print(page.links)

    end = time.time()
    # print(crawl.get_url_count())
    print("Took ", (end - start), " seconds")
