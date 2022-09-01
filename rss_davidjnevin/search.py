import re
from collections import namedtuple

import feedparser

DJN_FEED = "https://www.davidjnevin.com/index.xml"
DJN_BASEURL = "https://www.davidjnevin.com"
BLOG_MATCH = """Title: {title}
Link: {link}
"""
Blog = namedtuple("Blog", "title link")


class FeedSearcher:
    def __init__(self, feed=DJN_FEED):
        self.entries = feedparser.parse(feed).entries

    def _strip_html(self, text):
        return re.sub("<[^<]+?>", "", text)

    def _get_djn_link(self, link):
        # if the link is dirty then do some clean up here
        # slug = re.sub(r".*.com/(.*).mp3.*", r"\1", link)
        # return f"{DJN_BASEURL}/{slug}"
        return link

    def search(self, term):
        for entry in self.entries:
            title = entry.title
            term = term.lower()
            if term in entry.summary.lower() or term in title.lower():
                link = entry.links[0]["href"]
                link = self._get_djn_link(link)
                yield Blog(title, link)

    def _print_blog(self, blog):
        return BLOG_MATCH.format(title=blog.title, link=blog.link)

    def __call__(self):
        while True:
            term = input("Search for blogs ('q' for exit): ")
            term = term.strip().lower()
            if term == "q":
                print("Bye")
                break
            matching_blogs = list(self.search(term))
            if not matching_blogs:
                print("No hits, search again")
                continue
            for blog in matching_blogs:
                print(self._print_blog(blog))


def main():
    fs = FeedSearcher()
    fs()


if __name__ == "__main__":
    main()
