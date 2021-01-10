from dataclasses import dataclass
from typing import List

from takenote.gi_repository import GIRepository


Gdk = GIRepository.Gdk.load_binding()
Gtk = GIRepository.Gtk.load_binding()


@dataclass(frozen=True)
class NoteUI:

    note_window: Gtk.Window
    note_textview: Gtk.TextView
    lock_button: Gtk.Button
    move_button: Gtk.Button
    mode_button: Gtk.Button
    pin_button: Gtk.Button
    more_button: Gtk.Button
    resize_eventbox: Gtk.EventBox

    @classmethod
    def from_builder(cls, builder: Gtk.Builder):
        kwargs = {
            name: builder.get_object(name)
            for name in cls.__annotations__.keys()
            if not name.startswith("_")
        }

        ui = cls(**kwargs)
        return ui

    def set_style(self, provider: Gtk.CssProvider):
        widgets: List[Gtk.Widget] = [
            value for key, value in self.__dict__.items()
            if not key.startswith("_")
        ]
        for wgt in widgets:
            style_context = wgt.get_style_context()
            style_context.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def show(self):
        self.note_window.show()
