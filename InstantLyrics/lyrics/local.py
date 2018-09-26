# !/usr/bin/python3
# coding: utf-8

import os

from InstantLyrics.lyrics.models import LyricsFetcher


def get_local_lyrics_filename(query, folder):
    file_name = query.replace(" ", "_")
    file_name += ".txt"
    return os.path.join(folder, file_name)


class LocalLyricsFetcher(LyricsFetcher):
    """
    Searches for song lyrics in local folder
    """

    def __init__(self, folder):
        LyricsFetcher.__init__(self)
        self.search_folder = folder

    def get_available_lyrics(self):
        folder_content = os.listdir(self.search_folder)
        folder_content = [
            os.path.join(self.search_folder, f)  # full path
            for f in folder_content
        ]
        return [
            f
            for f in folder_content
            if os.path.isfile(f)  # just files
        ]

    def get_lyrics(self, query):
        print("Searching local folder for lyrics")

        available_lyrics = self.get_available_lyrics()
        lyrics_file = get_local_lyrics_filename(query, self.search_folder)
        if lyrics_file in available_lyrics:
            with open(lyrics_file, "r") as reader:
                return "".join(reader.readlines())  # content

        return None
