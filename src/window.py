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


@Gtk.Template(resource_path='/pm/mirko/Amusiz/window.ui')
class AmusizWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'AmusizWindow'

    btn_refresh = Gtk.Template.Child()
    entry_search = Gtk.Template.Child()
    scroll_window = Gtk.Template.Child()
    btn_about = Gtk.Template.Child()
    btn_help = Gtk.Template.Child()

    default_settings = Gtk.Settings.get_default()

    webview = webview.AmusizWebView()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        '''Prefer dark theme'''
        self.default_settings.set_property(
            "gtk-application-prefer-dark-theme",
            True
        )

        '''Signals'''
        self.btn_refresh.connect('pressed', self.webview.on_refresh)
        self.btn_about.connect('pressed', self.show_about)
        self.btn_help.connect('pressed', self.show_help)
        self.entry_search.connect('activate', self.webview.on_search)

        '''Show widgets'''
        self.scroll_window.add(self.webview.webview)
        self.show_all()

    @staticmethod
    def show_about(widget):
        about.AmusizAboutDialog().show_all()

    @staticmethod
    def show_help(widget):
        webbrowser.open("https://github.com/mirkobrombin/Amusiz")
