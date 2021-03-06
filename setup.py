# !/usr/bin/python3
# coding: utf_8

""" Setups library and install dependencies """

from glob import glob

from setuptools import setup, find_packages

DATA_FILES = [
    (
        'images', glob('icons/*')
    ),
]
DESCRIPTION = \
    "Instant-Lyrics\n\n\
    Instantly fetches the lyrics of the currently playing song and displays it on a window.\n\
    \n\
    Install\n\n\
    - $ pip3 install . --upgrade --force-reinstall, from the source\n\
    \n\
    Questions and issues\n\n\
    The Github issue tracker is only for bug reports and feature requests."

setup(
    name="Instant-Lyrics",
    version="2.0.1",
    author="sirfoga",
    author_email='captain.bhrigu@gmail.com,nicolas.guichard@ensimag.fr,'
                 'sirfoga@protonmail.com',
    description="Instantly fetches the lyrics of the currently playing song "
                "and displays it on a window.",
    long_description=DESCRIPTION,
    keywords="linux-app gtk3 pygobject lyrics spotify rhythmbox",
    url="https://github.com/sirfoga/Instant-Lyrics",
    packages=find_packages(),
    package_data={'': ['icons/*']},
    data_files=DATA_FILES,
    include_package_data=True,
    install_requires=[
        "requests",
        "beautifulsoup4",
        "lxml"
    ],
    entry_points={
        "console_scripts": [
            "instantlyrics = InstantLyrics.cmd:main"
        ]
    }
)
