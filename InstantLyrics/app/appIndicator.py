# !/usr/bin/python3
# coding: utf-8

import signal
import threading

import dbus
import gi
from dbus.mainloop.glib import DBusGMainLoop

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk
import os

from InstantLyrics.app.settings import APPINDICATOR_ID
from InstantLyrics.app.windows import LyricsWindow, PreferenceWindow
from InstantLyrics import utils


DBusGMainLoop(set_as_default=True)
ICON_PATH = utils.get_default_icon_path()  # full path
LOCAL_LYRICS_PATH = os.path.join(
    os.getenv("HOME"),
    ".local", "Instant-Lyrics", "lyrics"
)


def list_music_apps():
    apps = []
    session_bus = dbus.SessionBus()
    for service in session_bus.list_names():
        if service[:22] == "org.mpris.MediaPlayer2":
            apps.append(service[23:])

    return apps


class AppIndicator:
    def __init__(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        bus = dbus.SessionBus()

        bus.add_signal_receiver(self.build_menu, path="/org/mpris/MediaPlayer2")

        self.indicator = appindicator.Indicator.new(
            APPINDICATOR_ID, ICON_PATH,
            appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.build_menu()

        self.Config = utils.get_config()

        Gtk.main()

    def build_menu(self, *args):
        menu = Gtk.Menu()

        item_lyrics = Gtk.MenuItem('Custom Lyrics')
        item_lyrics.connect('activate', self.fetch_lyrics)
        menu.append(item_lyrics)

        for app in list_music_apps():
            current = Gtk.MenuItem(app.capitalize() + " lyrics")
            current.connect('activate', self.app_lyrics, app)
            menu.insert(current, 1)

        preferences = Gtk.MenuItem('Preferences')
        preferences.connect('activate', self.preferences)
        menu.append(preferences)

        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)

        menu.show_all()
        self.indicator.set_menu(menu)

    def fetch_lyrics(self, source):
        win = LyricsWindow("get", self)
        win.show_all()

    def app_lyrics(self, source, app):
        win = LyricsWindow("app", self)
        win.show_all()

        thread = threading.Thread(target=win.get_lyrics, args=(app,))
        thread.daemon = True
        thread.start()

    def preferences(self, source):
        win = PreferenceWindow(self)
        win.show_all()

    def quit(self, source):
        Gtk.main_quit()
