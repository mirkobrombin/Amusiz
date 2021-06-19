# window.py
#
# Copyright 2021 Mirko Brombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import webbrowser
from gi.repository import Gtk, Gdk, Gio, Handy, WebKit2
from pathlib import Path
from . import webview
from . import about
from . import preferences


@Gtk.Template(resource_path='/pm/mirko/Amusiz/window.ui')
class AmusizWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'AmusizWindow'

    btn_refresh = Gtk.Template.Child()
    entry_search = Gtk.Template.Child()
    scroll_window = Gtk.Template.Child()
    btn_preferences = Gtk.Template.Child()
    btn_about = Gtk.Template.Child()
    btn_help = Gtk.Template.Child()

    default_settings = Gtk.Settings.get_default()
    settings = Gio.Settings.new("pm.mirko.Amusiz")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Handy.init()

        self.webview = webview.AmusizWebView(self)

        '''Prefer dark theme'''
        self.default_settings.set_property(
            "gtk-application-prefer-dark-theme",
            True
        )

        '''Signals'''
        self.btn_refresh.connect('pressed', self.webview.on_refresh)
        self.btn_preferences.connect('pressed', self.show_preferences)
        self.btn_about.connect('pressed', self.show_about)
        self.btn_help.connect('pressed', self.show_help)
        self.entry_search.connect('key-release-event', self.webview.on_search)
        self.entry_search.connect('focus-in-event', self.webview.hit_element, "#navbarSearchInput")
        self.entry_search.connect('icon-release', self.webview.clear_search)
        self.settings.connect('changed', self.webview.start, "lang")

        '''Show widgets'''
        self.scroll_window.add(self.webview.webview)
        self.show_all()

    def show_preferences(self, widget):
        p = preferences.AmusizPreferences(self)
        p.present()

    def show_about(self, widget):
        about.AmusizAboutDialog(self).show_all()

    @staticmethod
    def show_help(widget):
        webbrowser.open("https://github.com/mirkobrombin/Amusiz")
