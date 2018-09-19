#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus


def get_lyrics(song_name):
    song_name += ' metrolyrics'
    name = quote_plus(song_name)
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'UPGRADE-INSECURE-REQUESTS': '1',
        'Connection': 'keep-alive'}

    url = 'https://www.google.com/search?q=' + name

    result = requests.get(url, headers=hdr).text
    link_start = result.find('http://www.metrolyrics.com')

    if (link_start == -1):
        return ("Lyrics not found on Metrolyrics")

    link_end = result.find('html', link_start + 1) + 4
    link = result[link_start:link_end]

    r = requests.get(link, headers=hdr)
    r.encoding = "utf-8"
    lyrics_html = r.text

    soup = BeautifulSoup(lyrics_html, "lxml")
    raw_lyrics = (soup.findAll('p', attrs={'class': 'verse'}))
    try:
        final_lyrics = unicode.join(u'\n', map(unicode, raw_lyrics))
    except NameError:
        final_lyrics = str.join(u'\n', map(str, raw_lyrics))

    final_lyrics = (final_lyrics.replace('<p class="verse">', '\n'))
    final_lyrics = (final_lyrics.replace('<br/>', ' '))
    final_lyrics = final_lyrics.replace('</p>', ' ')
    return (final_lyrics)
