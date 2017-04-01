#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk

import signal
import threading

from src.windows import LyricsWindow, PreferenceWindow
from . import utils
from src.settings import APPINDICATOR_ID, CONFIG_PATH

import dbus
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

class AppIndicator():
    def __init__(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        
        bus = dbus.SessionBus()
        
        bus.add_signal_receiver(self.build_menu, path="/org/mpris/MediaPlayer2")

        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, utils.get_icon_path(
'../icons/instant-lyrics-24.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.build_menu()
        
        self.Config = utils.get_config()
        
        Gtk.main()

    def list_apps(self):
        apps = []
        session_bus = dbus.SessionBus()
        for service in session_bus.list_names():
            if service[:22] == "org.mpris.MediaPlayer2":
                apps.append(service[23:])

        return apps

    def build_menu(self, *args):
        menu = Gtk.Menu()

        item_lyrics = Gtk.MenuItem('Custom Lyrics')
        item_lyrics.connect('activate', self.fetch_lyrics)
        menu.append(item_lyrics)

        apps = self.list_apps()
        for app in apps:
            current = Gtk.MenuItem(app.capitalize()+" lyrics")
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

    def app_lyrics(self, source, app):
        win = LyricsWindow("app", self)
        thread = threading.Thread(target=win.get_lyrics, args=(app,))
        thread.daemon = True
        thread.start()

    def preferences(self, source):
        win = PreferenceWindow(self)

    def quit(self, source):
        Gtk.main_quit()
