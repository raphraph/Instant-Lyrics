# !/usr/bin/python3
# coding: utf-8

import os

from InstantLyrics.lyrics.genius import LYRICS_FINDERS as GENIUS_FINDERS
from InstantLyrics.lyrics.local import LocalLyricsFetcher, \
    get_local_lyrics_filename
from InstantLyrics.lyrics.lyricstranslate import \
    LYRICS_FINDERS as LYRICSTRANSLATE_FINDERS
from InstantLyrics.lyrics.metrolyrics import \
    LYRICS_FINDERS as METROLYRICS_FINDERS

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
              ] + GENIUS_FINDERS + METROLYRICS_FINDERS + LYRICSTRANSLATE_FINDERS
    #finders = [LocalLyricsFetcher(LOCAL_LYRICS_FOLDER)]
    for finder in finders:
        try:
            result, source = finder.get_lyrics(query)
            print(source)
            #if result is not None:
            save_lyrics(query, result)  # save to local
            return result, source
        except:
            # nothing
            pass

    return None
