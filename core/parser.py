"""
Only Test in mikanani.me
"""
import re

import feedparser
import pandas
import logging
import requests
import bs4
import gc

logger = logging.getLogger(__name__)


class Parser:
    def __init__(self) -> None:
        pass

    @staticmethod
    def parseTorrentLink(entry: dict) -> str:
        """Get torrent link from rss feed entry

        Args:
            entry (dict): Rss feed entry

        Returns:
            str: torrent link
        """
        for link in entry.links:
            if link["type"] == "application/x-bittorrent":
                return link["href"]

    @staticmethod
    def parseAnimeName(home_page_url) -> str:
        try:
            resp = requests.get(home_page_url)
            soup = bs4.BeautifulSoup(resp.text, "html.parser")
            anime_name = soup.find("p", class_="bangumi-title").text.strip()
            # fix memory leak caused by BeautifulSoup
            resp.close()
            soup.decompose()
            soup = None
            gc.collect()
        except Exception as e:
            logger.error(f"Error when parsing anime name:{e}")
            return None
        return anime_name

    @staticmethod
    def parseDataFrame(
        feed: feedparser.FeedParserDict, filters: list[re.Pattern] = []
    ) -> pandas.DataFrame:
        """Parse rss feed from rss feed url to pandas.DataFrame
        with title, link, publish date

        Args:
            rss_url (dict): FeedParserDict generated by feedparser.parse()
            filters (list[re.Pattern], optional): Filter list. Defaults to [].

        Returns:
            pandas.DataFrame: With rss feed's title, link, publish date
        """
        data = {"title": [], "link": [], "pubDate": [], "animeName": []}
        for entry in feed.entries:
            match_result = True
            for pattern in filters:
                match_result = match_result and re.search(pattern, entry.title)
            if match_result:
                data["title"].append(entry.title)
                data["link"].append(Parser.parseTorrentLink(entry))
                data["pubDate"].append(entry.published)
                data["animeName"].append(Parser.parseAnimeName(entry.link))
        df = pandas.DataFrame(data)
        df["pubDate"] = pandas.to_datetime(df["pubDate"], format="mixed", utc=True)
        return df


if __name__ == "__main__":
    rssFilter = {
        "简体": r"(简体)|(简中)|(简日)|(CHS)",
        "繁体": r"(繁体)|(繁中)|(繁日)|(CHT)",
        "1080": r"(1080[pP])",
        "非合集": r"^((?!合集).)*$",
    }

    rss_url = "https://mikanani.me/RSS/Bangumi?bangumiId=2817"
    feed = feedparser.parse(rss_url)
    myfilter = [rssFilter["简体"], rssFilter["1080"]]
    df = Parser.parseDataFrame(feed, myfilter)
    print(df["title"])
    print(Parser.parseAnimeName(feed))