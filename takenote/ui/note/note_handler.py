from takenote.gi_repository import GIRepository
from takenote.notes_collection import NotesCollection
from takenote.resources.css import CSSResource
from takenote.resources.ui import UIResource
from takenote.ui.note.note_pin_mode import NotePinMode
from takenote.ui.note.note_ui import NoteUI

Gdk = GIRepository.Gdk.load_binding()
Gtk = GIRepository.Gtk.load_binding()


class NoteHandler:

    DEFAULT_PINMODE = NotePinMode.ABOVE

    def __init__(
            self,
            note_uuid: str,
            notes: NotesCollection,
            ui: NoteUI,
    ):
        self._note = notes.get_note(note_uuid)
        self._notes = notes
        self._ui = ui

        ui.move_window(self._note.position)
        ui.resize_window(self._note.size)

        # Load note UI with its text content.
        self._text_buffer: Gtk.TextBuffer = ui.note_textview.get_buffer()
        self._text_buffer.set_text(
            self._note.content,
            len(self._note.content.encode('utf-8'))
        )

        ui.note_textview.set_editable(not self._note.locked)

        self._set_pinning_mode(ui.note_window, self._note.pinmode)

    def on_resize_eventbox_button_press_event(self, window: Gtk.Window, event: Gdk.EventButton):
        window.begin_resize_drag(
            Gdk.WindowEdge.SOUTH_EAST,
            event.button,
            event.x_root,
            event.y_root,
            event.time
        )

    def on_move_button_button_press_event(self, window: Gtk.Window, event: Gdk.EventButton):
        window.begin_move_drag(
            event.button,
            event.x_root,
            event.y_root,
            event.time
        )

    def on_lock_button_clicked(self, textview: Gtk.TextView):
        self._note.locked = not self._note.locked
        textview.set_editable(not self._note.locked)

    def on_mode_button_clicked(self, window: Gtk.Window):
        self._toggle_pinning_mode(window)

    def on_pin_button_clicked(self, window: Gtk.Window):
        self._toggle_pinning(window)

    def on_note_textview_focus_out_event(self, widget: Gtk.Widget, event: Gdk.EventFocus):
        text = self._text_buffer.get_text(
            start=self._text_buffer.get_start_iter(),
            end=self._text_buffer.get_end_iter(),
            include_hidden_chars=False
        )

        root_x, root_y = self._ui.note_window.get_position()
        width, height = self._ui.note_window.get_size()

        self._note.content = text
        self._note.pinmode = self._note.pinmode
        self._note.set_position(root_x, root_y)
        self._note.set_size(height, width)
        self._note.save()

    def on_new_button_clicked(self, button: Gtk.Button):
        note = self._notes.add_note()
        ui = NoteHandler.attach_ui(self._notes, note.uuid)
        ui.show()

    def on_delete_button_clicked(self, window: Gtk.Window):
        self._notes.remove_note(self._note.uuid)
        window.close()

    def on_close_button_clicked(self, window: Gtk.Window):
        self._notes.set_note_ui(self._note.uuid, None)
        self._note.save()
        window.close()

    @staticmethod
    def on_more_button_clicked(popovermenu: Gtk.PopoverMenu):
        popovermenu.popup()

    @staticmethod
    def attach_ui(notes: NotesCollection, note_uuid: str) -> NoteUI:
        builder = Gtk.Builder.new_from_file(UIResource.NOTE_WINDOW.get_filename())

        note = notes.get_note(note_uuid)
        css_string = note._style.fill_css_template(
            CSSResource.TEMPLATE_NOTE_STYLE.get_filename())

        style_provider = Gtk.CssProvider.new()
        style_provider.load_from_data(css_string.encode("utf-8"))
        ui = NoteUI.from_builder(builder)
        ui.set_style(style_provider)
        notes.set_note_ui(note.uuid, ui)

        handler = NoteHandler(note.uuid, notes, ui)
        builder.connect_signals(handler)

        return ui

    def _toggle_pinning(self, window: Gtk.Window):
        self._note.pinmode = (
            NotePinMode.NONE
            if self._note.pinmode.ispinned
            else NoteHandler.DEFAULT_PINMODE
        )

        self._set_pinning_mode(window, self._note.pinmode)

    def _toggle_pinning_mode(self, window: Gtk.Window):
        # Toggle pinning mode.
        self._note.pinmode = (
            NotePinMode.BELOW
            if self._note.pinmode == NotePinMode.ABOVE
            else NotePinMode.ABOVE
        )

        if self._note.pinmode.ispinned:
            self._set_pinning_mode(window, self._note.pinmode)

    def _set_pinning_mode(self, window: Gtk.Window, pinmode: NotePinMode):
        type_hint = pinmode.gtk_window_typehint
        window.set_type_hint(type_hint)

        is_pinned = pinmode.ispinned
        self._ui.move_button.set_sensitive(not is_pinned)
        self._ui.resize_eventbox.set_visible(not is_pinned)
        self._ui.mode_button.set_visible(is_pinned)
