# !/usr/bin/python3
# coding: utf-8

from bs4 import BeautifulSoup

from lyrics.models import InternetLyricsFetcher


class GeniusFetcher(InternetLyricsFetcher):
    """
    Define abstract primitive operations that concrete subclasses define
    to implement steps of an algorithm.
    Implement a template method defining the skeleton of an algorithm.
    The template method calls primitive operations as well as operations
    defined in AbstractClass or those of other objects.
    """

    def __init__(self):
        InternetLyricsFetcher.__init__(
            self, 'https://genius.com'
        )

    def _parse_result(self, result):
        soup = BeautifulSoup(result, "lxml")
        raw = soup.findAll("div", {"class": "lyrics"})[0]
        parsed = raw.findAll("p")[0].text
        return parsed


class GoogleGeniusFetcher(GeniusFetcher):
    def _get_query(self, query):
        print("Searching google.com for genius.com lyrics")

        return 'site:genius.com ' + query  # search just genius

    def _get_url(self, query):
        return self.add_params_to_url("https://www.google.com/search", {
            "q": query
        })


class DuckDuckGoGeniusFetcher(GeniusFetcher):
    def _get_query(self, query):
        print("Searching duckduckgo.com for genius.com lyrics")

        return 'site:genius.com ' + query  # search just metrolyrics

    def _get_url(self, query):
        return self.add_params_to_url("https://duckduckgo.com/html", {
            "q": query
        })


LYRICS_FINDERS = [
    GoogleGeniusFetcher(),
    DuckDuckGoGeniusFetcher()
]
