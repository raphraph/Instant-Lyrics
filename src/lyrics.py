# !/usr/bin/python3
# coding: utf-8

import abc
import urllib.parse as urlparse
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) '
                  'Gecko/20100101 Firefox/52.0',
    'UPGRADE-INSECURE-REQUESTS': '1',
    'Connection': 'keep-alive'
}


def add_params_to_url(url, params):
    """
    :param url: str
        Url to add params to
    :param params: {}
        List of params to add to url
    :return: void
        Adds params to url
    """

    url_parts = list(urlparse.urlparse(url))  # get url parts
    query = dict(urlparse.parse_qsl(url_parts[4]))  # get url query
    query.update(params)  # add new params
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


class LyricsFetcher:
    """
    Searches for song lyrics in local folder
    """

    def __init__(self, query):
        self.query = query

    @abc.abstractclassmethod
    def get_lyrics(self):
        return None


class InternetLyricsFetcher(LyricsFetcher):
    """
    Searches internet for song lyrics
    """

    def __init__(self, query, search_engine):
        LyricsFetcher.__init__(self, query)
        self.url = search_engine

    def get_lyrics(self):
        try:
            link = self.get_lyrics_link()
            r = requests.get(link, headers=HEADERS)
            r.encoding = "utf-8"
            result = r.text
            return self._parse_result(result)
        except:
            return None

    def get_lyrics_link(self):
        query = self._get_query(self.query)
        url = self._get_url(query)
        response = requests.get(url, headers=HEADERS)
        result = response.text

        link_start = result.find(self.url)
        if link_start == -1:
            return None

        link_end = min(
            result.find('\'', link_start + 1),
            result.find('"', link_start + 1)
        )
        return result[link_start:link_end]

    @abc.abstractclassmethod
    def _parse_result(self, result):
        pass

    @abc.abstractmethod
    def _get_query(self, query):
        pass

    @abc.abstractmethod
    def _get_url(self, query):
        pass


class GeniusFetcher(InternetLyricsFetcher):
    """
    Define abstract primitive operations that concrete subclasses define
    to implement steps of an algorithm.
    Implement a template method defining the skeleton of an algorithm.
    The template method calls primitive operations as well as operations
    defined in AbstractClass or those of other objects.
    """

    def __init__(self, query):
        InternetLyricsFetcher.__init__(
            self, query, 'https://genius.com'
        )

    def _parse_result(self, result):
        soup = BeautifulSoup(result, "lxml")
        raw = soup.findAll("div", {"class": "lyrics"})[0]

        parsed = raw.findAll("p")[0].text
        # parsed = str.join(u'\n', map(str, parsed))

        if len(parsed) < 20:  # too little to be lyrcs => not found
            return None

        return parsed


class GoogleGeniusFetcher(GeniusFetcher):
    def _get_query(self, query):
        return 'site:genius.com ' + query  # search just genius

    def _get_url(self, query):
        return add_params_to_url("https://www.google.com/search", {
            "q": query
        })


class DuckDuckGoGeniusFetcher(GeniusFetcher):
    def _get_query(self, query):
        return 'site:genius.com ' + query  # search just metrolyrics

    def _get_url(self, query):
        return add_params_to_url("https://duckduckgo.com/html", {
            "q": query
        })


class MetrolyricsFetcher(InternetLyricsFetcher):
    """
    Define abstract primitive operations that concrete subclasses define
    to implement steps of an algorithm.
    Implement a template method defining the skeleton of an algorithm.
    The template method calls primitive operations as well as operations
    defined in AbstractClass or those of other objects.
    """

    def __init__(self, query):
        InternetLyricsFetcher.__init__(
            self, query, 'http://www.metrolyrics.com'
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
        return add_params_to_url("https://www.google.com/search", {
            "q": query
        })


class DuckDuckGoMetrolyricsFetcher(MetrolyricsFetcher):
    def _get_query(self, query):
        return 'site:metrolyrics.com ' + query  # search just metrolyrics

    def _get_url(self, query):
        return add_params_to_url("https://duckduckgo.com/html", {
            "q": query
        })


def get_lyrics(query):
    return GoogleMetrolyricsFetcher(query).get_lyrics()
