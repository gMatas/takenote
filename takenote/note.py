import enum

from pkg_resources import resource_filename

from takenote.resources.ui import UIResource
from takenote.gi_repository import Gtk, Gdk


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
            builder: Gtk.Builder,
            ispinned: bool = False,
            pinmode: NotePinMode = NotePinMode.ABOVE
    ):
        self._ispinned = ispinned
        self._pinmode = pinmode

        self._resize_button: Gtk.Button = builder.get_object('resize_button')
        self._move_button: Gtk.Button = builder.get_object('move_button')
        self._pin_button: Gtk.Button = builder.get_object('pin_button')
        self._mode_button: Gtk.Button = builder.get_object('mode_button')

        self._mode_button.set_visible(self._ispinned)

    def on_close_button_clicked(self, window: Gtk.Window):
        window.close()

    def on_resize_button_press_event(self, window: Gtk.Window, eventbutton: Gdk.EventButton):
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

    def on_more_button_clicked(self, popovermenu: Gtk.PopoverMenu):
        popovermenu.popup()

    def on_pin_button_clicked(self, window: Gtk.Window):
        self._toggle_pinning(window)

        self._resize_button.set_sensitive(not self._ispinned)
        self._move_button.set_sensitive(not self._ispinned)

        self._mode_button.set_visible(self._ispinned)

    def on_new_button_clicked(self, button: Gtk.Button):
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
        # Toggle pinning mode between ``ABOVE`` and ``BELOW`` options.
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
        ui_filepath = resource_filename('takenote.resources.ui', 'note.glade')
        builder = Gtk.Builder.new_from_file(ui_filepath)

        handler = NoteHandler(builder)
        builder.connect_signals(handler)

        self._window: Gtk.Window = builder.get_object('note_window')

    def show(self):
        self._window.show()
