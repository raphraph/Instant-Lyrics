# !/usr/bin/python3
# coding: utf-8

from lyrics.genius import GoogleGeniusFetcher


def get_lyrics(query):
    return GoogleGeniusFetcher(query).get_lyrics()
