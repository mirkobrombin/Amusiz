# webview.py
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

import webbrowser
import urllib.parse
from gi.repository import Gtk, Gdk, Gio, Handy, WebKit2
from .globals import amazon_uris, cookies_path


class AmusizWebSettings(WebKit2.Settings):

    hw_accell = WebKit2.HardwareAccelerationPolicy.NEVER

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_hardware_acceleration_policy(self.hw_accell)
        self.set_enable_back_forward_navigation_gestures(True)
        self.set_enable_dns_prefetching(True)
        self.set_enable_media_capabilities(True)
        # self.set_enable_smooth_scrolling(True)
        self.set_enable_developer_extras(True)


class AmusizContentManager(WebKit2.UserContentManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        '''CSS tricks'''
        style = Gio.resources_lookup_data("/pm/mirko/Amusiz/inject.css", 0)
        self.add_style_sheet(
            WebKit2.UserStyleSheet(
                str(style.get_data(), "utf-8"),
                WebKit2.UserContentInjectedFrames.TOP_FRAME,
                WebKit2.UserStyleLevel.USER,
                None, None
            )
        )


class AmusizWebView():

    context = WebKit2.WebContext.get_default()
    manager = AmusizContentManager()
    settings = AmusizWebSettings()
    policies = WebKit2.WebsitePolicies(autoplay=WebKit2.AutoplayPolicy.ALLOW)
    webview = WebKit2.WebView(
        settings=settings,
        user_content_manager=manager,
        website_policies=policies
    )
    cookies = context.get_cookie_manager()
    cookies.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)

        self.window = window
        self.start()

        '''Signals'''
        self.webview.connect('load-changed', self.on_change)
        self.webview.connect('load-failed-with-tls-errors', self.on_tls_errors)

        '''Webview'''
        self.webview.set_background_color(Gdk.RGBA(0.05, 0.05, 0.05, 1.0))

        '''Cookies'''
        self.cookies.set_persistent_storage(
            cookies_path,
            WebKit2.CookiePersistentStorage.SQLITE
        )

    '''Webview methods'''

    def start(self, settings=False, key=None, user_data=None):
        lang = self.window.settings.get_string("lang")
        self.amazon_uri = amazon_uris[lang]
        self.webview.load_uri(self.amazon_uri)

    def hit_element(self, widget=None, user_data=None, element="body"):
        script = f"document.querySelector('{element}').click();"
        self.webview.run_javascript(script)

    def open_browser(self, widget=None, url="about:blank"):
        webbrowser.open(url)

    def open_url(self, widget=None, url="about:blank"):
        self.webview.load_uri(url)

    def on_tls_errors(self, widget, failing_uri, certificate, errors):
        host = urllib.parse.urlparse(failing_uri).netloc
        ctx = self.webview.get_context()
        ctx.allow_tls_certificate_for_host(certificate, host)

    def on_refresh(self, widget=None):
        self.webview.reload()

    def clear_search(self, widget, icon_pos, event, user_data=None):
        self.on_search(widget, Gdk.KEY_Escape)

    def perform_adv_search(self, widget=None, data=None):
        terms = widget.get_text()
        url = f"{self.amazon_uri}/search/{terms}"
        self.webview.load_uri(url)

    def on_search(self, widget=None, event=None, data=None):
        if event == Gdk.KEY_Escape or event.keyval == Gdk.KEY_Escape:
                widget.set_text("")

        terms = widget.get_text()
        script = f"""
        document.getElementById("navbarSearchInput").value ="{terms}";
        var event = document.createEvent('Event');
        event.initEvent('input', true, true);
        document.getElementById("navbarSearchInput").dispatchEvent(event);
        """
        self.webview.run_javascript(script)

    def on_change(self, web_view, load_event):
        scripts = Gio.resources_lookup_data("/pm/mirko/Amusiz/scripts.js", 0)
        self.webview.run_javascript(str(scripts.get_data(), "utf-8"))


