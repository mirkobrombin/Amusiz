# preferences.py
#
# Copyright 2020 brombinmirko <send@mirko.pm>
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

from gi.repository import Gtk, GLib, Handy

langs = ["US", "IT", "FR", "DE"]

@Gtk.Template(resource_path='/pm/mirko/Amusiz/preferences.ui')
class AmusizPreferences(Handy.PreferencesWindow):
    __gtype_name__ = 'AmusizPreferences'

    '''Get widgets from template'''
    combo_lang = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.set_transient_for(window)

        '''Common variables'''
        self.window = window
        self.settings = window.settings
        self.default_settings = window.default_settings

        '''Set widgets status from user settings'''
        # self.combo_lang.set_active(self.settings.get_boolean("lang"))

        '''Signal connections'''
        # self.combo_lang.connect('state-set', self.toggle_dark)


