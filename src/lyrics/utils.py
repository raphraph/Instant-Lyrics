# !/usr/bin/python3
# coding: utf-8

import os

from lyrics.genius import LYRICS_FINDERS as GENIUS_FINDERS
from lyrics.metrolyrics import LYRICS_FINDERS as METROLYRICS_FINDERS
from .local import LocalLyricsFetcher, get_local_lyrics_filename

LOCAL_LYRICS_FOLDER = os.path.join(
    os.getenv("HOME"),
    ".local", "Instant-Lyrics", "lyrics"
)

if not os.path.exists(LOCAL_LYRICS_FOLDER):
    os.makedirs(LOCAL_LYRICS_FOLDER)  # make sure there is a local folder


def save_lyrics(query, lyrics):
    file_name = get_local_lyrics_filename(query, LOCAL_LYRICS_FOLDER)
    while "\n\n" in lyrics:  # remove double line endings
        lyrics = lyrics.replace("\n\n", "\n")

    with open(file_name, "w") as writer:
        writer.write(lyrics)


def get_lyrics(query):
    finders = [
                  LocalLyricsFetcher(LOCAL_LYRICS_FOLDER)  # local
              ] + GENIUS_FINDERS + METROLYRICS_FINDERS  # internet

    for finder in finders:
        result = finder.get_lyrics(query)
        if result is not None:
            save_lyrics(query, result)  # save to local
            return result

    return None