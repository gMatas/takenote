from dataclasses import dataclass
import enum
from typing import List

from takenote.gi_repository import GIRepository
from takenote.resources.css import CSSResource
from takenote.resources.ui import UIResource


# Linter friendly GI bindings.
Gdk = GIRepository.Gdk.load_binding()
Gtk = GIRepository.Gtk.load_binding()


@dataclass(frozen=True)
class NoteUI:

    note_window: Gtk.Window
    text_view: Gtk.TextView
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
            if not name.startswith('_')
        }

        note_ui = cls(**kwargs)
        return note_ui

    def set_style(self, provider: Gtk.CssProvider):
        widgets: List[Gtk.Widget] = [
            value for key, value in self.__dict__.items()
            if not key.startswith('_')
        ]
        for wgt in widgets:
            style_context = wgt.get_style_context()
            style_context.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class NotePinMode(enum.Enum):

    ABOVE = enum.auto()
    BELOW = enum.auto()


class NoteHandler:

    _DEFAULT_PINMODE = NotePinMode.ABOVE
    _PINMODE_TYPE_HINTS = {
        NotePinMode.ABOVE: Gdk.WindowTypeHint.DOCK,
        NotePinMode.BELOW: Gdk.WindowTypeHint.DESKTOP,
    }

    def __init__(
            self,
            ui: NoteUI,
            ispinned: bool = False,
            pinmode: NotePinMode = NotePinMode.ABOVE
    ):
        self._ui = ui
        self._ispinned = ispinned
        self._pinmode = pinmode

        self._ui.mode_button.set_visible(self._ispinned)

    def on_resize_eventbox_press_event(self, window: Gtk.Window, eventbutton: Gdk.EventButton):
        if self._ispinned:
            return

        window.begin_resize_drag(
            Gdk.WindowEdge.SOUTH_EAST,
            eventbutton.button,
            eventbutton.x_root,
            eventbutton.y_root,
            eventbutton.time
        )

    def on_move_button_press_event(self, window: Gtk.Window, eventbutton: Gdk.EventButton):
        if self._ispinned:
            return

        window.begin_move_drag(
            eventbutton.button,
            eventbutton.x_root,
            eventbutton.y_root,
            eventbutton.time
        )

    def on_mode_button_clicked(self, window: Gtk.Window):
        self._toggle_pinning_mode(window)

    def on_pin_button_clicked(self, window: Gtk.Window):
        self._toggle_pinning(window)

        self._ui.move_button.set_sensitive(not self._ispinned)

        self._ui.resize_eventbox.set_visible(not self._ispinned)
        self._ui.mode_button.set_visible(self._ispinned)

    @staticmethod
    def on_close_button_clicked(window: Gtk.Window):
        window.close()

    @staticmethod
    def on_more_button_clicked(popovermenu: Gtk.PopoverMenu):
        popovermenu.popup()

    @staticmethod
    def on_new_button_clicked(button: Gtk.Button):
        note = Note()
        note.show()

    def _toggle_pinning(self, window: Gtk.Window):
        if not self._ispinned:
            self._pinmode = NoteHandler._DEFAULT_PINMODE

        type_hint = (
            Gdk.WindowTypeHint.UTILITY
            if self._ispinned
            else NoteHandler._PINMODE_TYPE_HINTS[self._pinmode]
        )
        window.set_type_hint(type_hint)

        self._ispinned = not self._ispinned

    def _toggle_pinning_mode(self, window: Gtk.Window):
        # Toggle pinning mode.
        self._pinmode = (
            NotePinMode.BELOW
            if self._pinmode == NotePinMode.ABOVE
            else NotePinMode.ABOVE
        )

        # Apply new pinning mode.
        if self._ispinned:
            type_hint = NoteHandler._PINMODE_TYPE_HINTS[self._pinmode]
            window.set_type_hint(type_hint)


class Note:

    def __init__(self):
        builder = Gtk.Builder.new_from_file(UIResource.NOTE_WINDOW.get_filename())

        style_provider = Gtk.CssProvider.new()
        style_provider.load_from_path(CSSResource.NOTE_STYLE.get_filename())
        ui = NoteUI.from_builder(builder)
        ui.set_style(style_provider)

        handler = NoteHandler(ui)
        builder.connect_signals(handler)

        self._ui = ui

    @classmethod
    def show_window(cls):
        cls().show()

    def show(self):
        return self._ui.note_window.show()


if __name__ == '__main__':
    Note.show_window()
    Gtk.main()
