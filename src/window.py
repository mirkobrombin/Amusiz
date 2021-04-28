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

from gi.repository import Gtk, Handy, WebKit2

@Gtk.Template(resource_path='/pm/mirko/Amusiz/window.ui')
class AmusizWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'AmusizWindow'

    btn_refresh = Gtk.Template.Child()
    entry_search = Gtk.Template.Child()
    scroll_window = Gtk.Template.Child()
    default_settings = Gtk.Settings.get_default()
    amazon_uri = "https://music.amazon.it"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.default_settings.set_property(
            "gtk-application-prefer-dark-theme", True)

        '''Signals'''
        self.btn_refresh.connect('pressed', self.on_refresh)
        self.entry_search.connect('activate', self.on_search)

        '''Webview'''
        context = WebKit2.WebContext.get_default()
        manager = WebKit2.UserContentManager()
        self.webview = WebKit2.WebView.new_with_user_content_manager(manager)
        self.webview.load_uri(self.amazon_uri)

        '''Settings & Cookies'''
        cookies = context.get_cookie_manager()
        cookies.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)
        cookies.set_persistent_storage(
            '/tmp/cookies.txt',
            WebKit2.CookiePersistentStorage.TEXT
        )

        self.scroll_window.add(self.webview)
        self.show_all()

    def on_refresh(self, widget):
        self.webview.reload()

    def on_search(self, widget):
        terms = widget.get_text()
        self.webview.load_uri(f"{self.amazon_uri}/search/{terms}")
