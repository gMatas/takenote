import os

from gi.repository import Gtk

from takenote.constants import ICONS_PATH, ICONS_THEME_NAME, NOTES_DATA_PATH
from takenote.notes_collection import NotesCollection


class TakenoteContext:

    def __init__(self):
        self.notes = (
            NotesCollection.load(NOTES_DATA_PATH)
            if os.path.exists(NOTES_DATA_PATH)
            else NotesCollection()
        )

        self.icon_theme = Gtk.IconTheme.new()
        self.icon_theme.append_search_path(ICONS_PATH)
        self.icon_theme.set_custom_theme(ICONS_THEME_NAME)
