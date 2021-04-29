# main.py
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

import sys
import gi
import webbrowser

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, Gdk, Gio, Handy

from .window import AmusizWindow


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='pm.mirko.Amusiz',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.set_actions()

    def do_activate(self):
        '''Load custom CSS'''
        data_bytes = Gio.resources_lookup_data(
            "/pm/mirko/Amusiz/style.css", 0)
        provider = Gtk.CssProvider()
        provider.load_from_data(data_bytes.get_data())
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
                                                 provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        win = self.props.active_window
        if not win:
            win = AmusizWindow(application=self)

        self.win = win
        win.present()


    def quit(self, action=None, param=None):
        '''Quit application [CTRL+Q]'''
        self.win.destroy()

    @staticmethod
    def help(action, param):
        '''Open Help URL [F1]'''
        webbrowser.open_new_tab("https://github.com/mirkobrombin/Amusiz")

    def refresh(self, action, param):
        '''Refresh [CTRL+R]'''
        self.win.on_refresh()

    def set_actions(self):
        '''Register window actions'''
        action_entries = [
            ("quit", self.quit, ("app.quit", ["<Ctrl>Q"])),
            ("help", self.help, ("app.help", ["F1"])),
            ("refresh", self.refresh, ("app.refresh", ["<Ctrl>R"]))
        ]

        for action, callback, accel in action_entries:
            simple_action = Gio.SimpleAction.new(action, None)
            simple_action.connect('activate', callback)
            self.add_action(simple_action)
            if accel is not None:
                self.set_accels_for_action(*accel)


def main(version):
    app = Application()
    return app.run(sys.argv)
