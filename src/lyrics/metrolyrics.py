# !/usr/bin/python3
# coding: utf-8

from bs4 import BeautifulSoup

from .models import InternetLyricsFetcher


class MetrolyricsFetcher(InternetLyricsFetcher):
    """
    Define abstract primitive operations that concrete subclasses define
    to implement steps of an algorithm.
    Implement a template method defining the skeleton of an algorithm.
    The template method calls primitive operations as well as operations
    defined in AbstractClass or those of other objects.
    """

    def __init__(self):
        InternetLyricsFetcher.__init__(
            self, 'http://www.metrolyrics.com'
        )

    def _parse_result(self, result):
        soup = BeautifulSoup(result, "lxml")
        raw = (soup.findAll('p', attrs={'class': 'verse'}))

        parsed = str.join(u'\n', map(str, raw))
        parsed = parsed.replace('<p class="verse">', '\n')
        parsed = parsed.replace('<br/>', ' ')
        parsed = parsed.replace('</p>', ' ')
        parsed = parsed.strip()

        if len(parsed) < 20:  # too little to be lyrcs => not found
            return None

        return parsed


class GoogleMetrolyricsFetcher(MetrolyricsFetcher):
    def _get_query(self, query):
        return 'site:metrolyrics.com ' + query  # search just metrolyrics

    def _get_url(self, query):
        return self.add_params_to_url("https://www.google.com/search", {
            "q": query
        })


class DuckDuckGoMetrolyricsFetcher(MetrolyricsFetcher):
    def _get_query(self, query):
        return 'site:metrolyrics.com ' + query  # search just metrolyrics

    def _get_url(self, query):
        return self.add_params_to_url("https://duckduckgo.com/html", {
            "q": query
        })


LYRICS_FINDERS = [
    GoogleMetrolyricsFetcher(),
    DuckDuckGoMetrolyricsFetcher()
]
