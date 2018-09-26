# !/usr/bin/python3
# coding: utf-8

import os

from .models import LyricsFetcher


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
        return [
            os.path.join(self.search_folder, f)  # full path
            for f in folder_content
            if os.path.isfile(f)  # just files
        ]

    def get_lyrics(self, query):
        lyrics_file = get_local_lyrics_filename(self.query, self.search_folder)
        if lyrics_file in self.get_available_lyrics():
            print("Fetching lyrics from", lyrics_file)

            with open(lyrics_file, "r") as reader:
                lines = reader.readlines()
                return "\n".join(lines)  # content

        return None
