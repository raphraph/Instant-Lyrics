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


class MetrolyricsFetcher:
    """
    Define abstract primitive operations that concrete subclasses define
    to implement steps of an algorithm.
    Implement a template method defining the skeleton of an algorithm.
    The template method calls primitive operations as well as operations
    defined in AbstractClass or those of other objects.
    """

    def __init__(self, query):
        self.query = query

    def get_lyrics(self):
        query = self._get_query(self.query)
        url = self._get_url(query)
        response = requests.get(url, headers=HEADERS)
        result = response.text
        link_start = result.find('http://www.metrolyrics.com')
        return link_start, result

    @abc.abstractmethod
    def _get_query(self, query):
        pass

    @abc.abstractmethod
    def _get_url(self, query):
        pass


class GoogleMetrolyricsFetcher(MetrolyricsFetcher):
    def _get_query(self, query):
        return query + ' metrolyrics:'  # search just metrolyrics

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
    link_start, result = DuckDuckGoMetrolyricsFetcher(query).get_lyrics()

    if link_start == -1:
        return None

    link_end = result.find('html', link_start + 1) + 4
    link = result[link_start:link_end]

    r = requests.get(link, headers=HEADERS)
    r.encoding = "utf-8"
    lyrics_html = r.text

    soup = BeautifulSoup(lyrics_html, "lxml")
    raw_lyrics = (soup.findAll('p', attrs={'class': 'verse'}))
    final_lyrics = str.join(u'\n', map(str, raw_lyrics))

    final_lyrics = final_lyrics.replace('<p class="verse">', '\n')
    final_lyrics = final_lyrics.replace('<br/>', ' ')
    final_lyrics = final_lyrics.replace('</p>', ' ')
    final_lyrics = final_lyrics.strip()

    if len(final_lyrics) < 20:  # too little to be lyrcs => not found
        return None

    return final_lyrics
