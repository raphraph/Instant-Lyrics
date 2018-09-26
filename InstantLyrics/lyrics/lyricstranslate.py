# !/usr/bin/python3
# coding: utf-8

from bs4 import BeautifulSoup

from InstantLyrics.lyrics.models import InternetLyricsFetcher


class LyricsTranslateFetcher(InternetLyricsFetcher):
    """
    Define abstract primitive operations that concrete subclasses define
    to implement steps of an algorithm.
    Implement a template method defining the skeleton of an algorithm.
    The template method calls primitive operations as well as operations
    defined in AbstractClass or those of other objects.
    """

    def __init__(self):
        InternetLyricsFetcher.__init__(
            self, 'https://lyricstranslate.com/'
        )

    def _parse_result(self, result):
        soup = BeautifulSoup(result, "lxml")
        raw = soup.findAll("div", {"class": "ltf"})[0]
        parsed = raw.text
        return parsed


class GoogleLyricstranslateFetcher(LyricsTranslateFetcher):
    def _get_query(self, query):
        print("Searching google.com for lyricstranslate.com lyrics")

        return 'site:lyricstranslate.com ' + query  # search just genius

    def _get_url(self, query):
        return self.add_params_to_url("https://www.google.com/search", {
            "q": query
        })


class DuckDuckGoLyricstranslateFetcher(LyricsTranslateFetcher):
    def _get_query(self, query):
        print("Searching duckduckgo.com for lyricstranslate.com lyrics")

        return 'site:lyricstranslate.com ' + query  # search just metrolyrics

    def _get_url(self, query):
        return self.add_params_to_url("https://duckduckgo.com/html", {
            "q": query
        })


LYRICS_FINDERS = [
    GoogleLyricstranslateFetcher(),
    DuckDuckGoLyricstranslateFetcher()
]
