from takenote.gi_repository import GIRepository
from takenote.notes_collection import NotesCollection
from takenote.resources.css import CSSResource
from takenote.resources.ui import UIResource
from takenote.ui.note.note_pin_mode import NotePinMode
from takenote.ui.note.note_ui import NoteUI


Gdk = GIRepository.Gdk.load_binding()
Gtk = GIRepository.Gtk.load_binding()


class NoteUIHandler:

    DEFAULT_PINMODE = NotePinMode.ABOVE

    def __init__(
            self,
            ui: NoteUI,
            notes: NotesCollection,
            note_uuid: str,
            pinmode: NotePinMode = NotePinMode.NONE
    ):
        self._ui = ui
        self._note = notes.get_note(note_uuid)
        self._notes = notes
        self._pinmode = pinmode

        self._text_buffer: Gtk.TextBuffer = self._ui.note_textview.get_buffer()

        self._ui.mode_button.set_visible(self._pinmode.ispinned)

    def on_resize_eventbox_press_event(self, window: Gtk.Window, eventbutton: Gdk.EventButton):
        if self._pinmode.ispinned:
            return

        window.begin_resize_drag(
            Gdk.WindowEdge.SOUTH_EAST,
            eventbutton.button,
            eventbutton.x_root,
            eventbutton.y_root,
            eventbutton.time
        )

    def on_move_button_press_event(self, window: Gtk.Window, eventbutton: Gdk.EventButton):
        if self._pinmode.ispinned:
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

        self._ui.move_button.set_sensitive(not self._pinmode.ispinned)

        self._ui.resize_eventbox.set_visible(not self._pinmode.ispinned)
        self._ui.mode_button.set_visible(self._pinmode.ispinned)

    def on_note_textview_focus_out_event(self, widget: Gtk.Widget, event: Gdk.EventFocus):
        text = self._text_buffer.get_text(
            start=self._text_buffer.get_start_iter(),
            end=self._text_buffer.get_end_iter(),
            include_hidden_chars=False
        )

        self._note.content = text
        self._note.pinmode = self._pinmode
        self._note.save()

    def on_new_button_clicked(self, button: Gtk.Button):
        note = self._notes.add_note()
        ui = NoteUIHandler.create_ui(self._notes, note.uuid)
        ui.show()

    def on_close_button_clicked(self, window: Gtk.Window):
        self._note.save()
        window.close()

    @staticmethod
    def on_more_button_clicked(popovermenu: Gtk.PopoverMenu):
        popovermenu.popup()

    @staticmethod
    def create_ui(notes: NotesCollection, note_uuid: str) -> NoteUI:
        builder = Gtk.Builder.new_from_file(UIResource.NOTE_WINDOW.get_filename())

        style_provider = Gtk.CssProvider.new()
        style_provider.load_from_path(CSSResource.NOTE_STYLE.get_filename())

        ui = NoteUI.from_builder(builder)
        ui.set_style(style_provider)

        note = notes.get_note(note_uuid)
        handler = NoteUIHandler(ui, notes, note.uuid)

        builder.connect_signals(handler)

        return ui

    def _toggle_pinning(self, window: Gtk.Window):
        self._pinmode = (
            NotePinMode.NONE
            if self._pinmode.ispinned
            else NoteUIHandler.DEFAULT_PINMODE
        )

        type_hint = self._pinmode.gtk_window_typehint
        window.set_type_hint(type_hint)

    def _toggle_pinning_mode(self, window: Gtk.Window):
        # Toggle pinning mode.
        self._pinmode = (
            NotePinMode.BELOW
            if self._pinmode == NotePinMode.ABOVE
            else NotePinMode.ABOVE
        )

        # Apply new pinning mode.
        if self._pinmode.ispinned:
            type_hint = self._pinmode.gtk_window_typehint
            window.set_type_hint(type_hint)
