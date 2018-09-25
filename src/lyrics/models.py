# !/usr/bin/python3
# coding: utf-8

import abc
import urllib.parse as urlparse
from urllib.parse import urlencode

import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) '
                  'Gecko/20100101 Firefox/52.0',
    'UPGRADE-INSECURE-REQUESTS': '1',
    'Connection': 'keep-alive'
}


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

    @staticmethod
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
