# !/usr/bin/python3
# coding: utf-8

import os

from .models import LyricsFetcher


class LocalLyricsFetcher(LyricsFetcher):
    """
    Searches for song lyrics in local folder
    """

    def __init__(self, query, folder):
        LyricsFetcher.__init__(self, query)
        self.search_folder = folder

    def get_available_lyrics(self):
        folder_content = os.listdir(self.search_folder)
        return [
            os.path.join(self.search_folder, f)  # full path
            for f in folder_content
            if os.path.isfile(f)  # just files
        ]

    def get_lyrics(self):
        lyrics_file = self.get_query_file()
        if lyrics_file in self.get_available_lyrics():
            with open(lyrics_file, "r") as reader:
                lines = reader.readlines()
                return "\n".join(lines)  # content

        return None

    def get_query_file(self):
        file_name = self.query.replace(" ", "_")
        return os.path.join(self.search_folder, file_name)
