# !/usr/bin/python3
# coding: utf-8

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
BASE_URL = "https://www.google.com/search"


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


def get_metrolyrics_from_google(query):
    query += ' metrolyrics:'  # search just metrolyrics
    url = add_params_to_url(BASE_URL, {
        "q": query
    })
    response = requests.get(url, headers=HEADERS)
    result = response.text
    link_start = result.find('http://www.metrolyrics.com')
    return link_start, result


def get_lyrics(query):
    link_start, result = get_metrolyrics_from_google(query)

    if link_start == -1:
        return "Lyrics not found"

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
    return final_lyrics
