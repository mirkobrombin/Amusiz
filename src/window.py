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
from gi.repository import Gtk, Gdk, Gio, Handy, WebKit2
from pathlib import Path

@Gtk.Template(resource_path='/pm/mirko/Amusiz/window.ui')
class AmusizWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'AmusizWindow'

    btn_refresh = Gtk.Template.Child()
    entry_search = Gtk.Template.Child()
    scroll_window = Gtk.Template.Child()

    amazon_uri = "https://music.amazon.it"
    cookies_path = f"{Path.home()}/.cache/cookies.txt"

    default_settings = Gtk.Settings.get_default()
    context = WebKit2.WebContext.get_default()
    manager = WebKit2.UserContentManager()
    settings = WebKit2.Settings()
    webview = WebKit2.WebView.new_with_user_content_manager(manager)
    cookies = context.get_cookie_manager()
    cookies.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)

    st_hw_accell = WebKit2.HardwareAccelerationPolicy.NEVER

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if "SNAP" in os.environ:
            self.cookies_path = f"{os.environ['SNAP_USER_DATA']}/cookies.txt"

        '''Prefer dark theme'''
        self.default_settings.set_property(
            "gtk-application-prefer-dark-theme", True)

        '''Signals'''
        self.btn_refresh.connect('pressed', self.on_refresh)
        self.entry_search.connect('activate', self.on_search)
        self.webview.connect('load-changed', self.on_change)

        '''Webview'''
        self.webview.load_uri(self.amazon_uri)
        self.webview.get_style_context().add_class("webview")
        self.webview.set_background_color(Gdk.RGBA(0.05,0.05,0.05,1.0))

        '''Settings'''
        self.settings.set_hardware_acceleration_policy(self.st_hw_accell)
        # self.settings.set_enable_smooth_scrolling(True)
        self.webview.set_settings(self.settings)

        '''Cookies'''
        self.cookies.set_persistent_storage(
            self.cookies_path,
            WebKit2.CookiePersistentStorage.TEXT
        )

        '''CSS tricks'''
        style = WebKit2.UserStyleSheet("""
            #navbarSearchInput,#navbarSearchInputButton {
                display:none !important;
            }
            #navbar {
                height: 64px !important;
            }
            #navbar, #contextMenuOverlay > div {
                background-color: #000 !important;
            }
            #contextMenuOverlay > div {
                padding: 5px 0 !important;
            }
            """,
            WebKit2.UserContentInjectedFrames.TOP_FRAME,
            WebKit2.UserStyleLevel.USER,
            None, None
        )
        self.manager.add_style_sheet(style)

        self.scroll_window.add(self.webview)
        self.show_all()

    def on_refresh(self, widget=None):
        self.webview.reload()
        # self.webview.get_inspector()

    def on_search(self, widget):
        terms = widget.get_text()
        self.webview.load_uri(f"{self.amazon_uri}/search/{terms}")

    def on_change(self, web_view, load_event):
        scripts = Gio.resources_lookup_data("/pm/mirko/Amusiz/scripts.js", 0)
        self.webview.run_javascript(str(scripts.get_data(), "utf-8"))


