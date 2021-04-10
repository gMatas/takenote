from gi.repository import Gdk, Gtk

from takenote.context import TakenoteContext
from takenote.icon_theme import TakenoteIcon
from takenote.resources.css import CSSResource
from takenote.resources.ui import UIResource
from takenote.ui.note.note_pin_mode import NotePinMode
from takenote.ui.note.note_ui import NoteUI


class NoteHandler:

    DEFAULT_PINMODE = NotePinMode.ABOVE

    def __init__(
            self,
            context: TakenoteContext,
            note_uuid: str,
            ui: NoteUI,
    ):
        self._note = context.notes.get_note(note_uuid)
        self._context = context
        self._ui = ui

        ui.move_window(self._note.position)
        ui.resize_window(self._note.size)

        # Load note UI with its text content.
        self._text_buffer: Gtk.TextBuffer = ui.note_textview.get_buffer()
        self._text_buffer.set_text(
            self._note.content,
            len(self._note.content.encode("utf-8"))
        )

        ui.note_textview.set_editable(not self._note.locked)
        ui.note_textview.set_cursor_visible(not self._note.locked)
        
        # Default static icons.
        self._set_button_icon(ui.pin_button, TakenoteIcon.PUSH_PIN)
        self._set_button_icon(ui.more_button, TakenoteIcon.VIEW_MORE)

        # Default dynamic icons.
        self._set_pinning_mode(ui.note_window)
        self._update_lock_icon()

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
        textview.set_cursor_visible(not self._note.locked)
        self._update_lock_icon()
        
    def on_mode_button_clicked(self, window: Gtk.Window):
        self._toggle_pinning_mode(window)

    def on_pin_button_clicked(self, window: Gtk.Window):
        self._toggle_pinning(window)

    def on_note_window_button_press_event(self, widget, event):
        # print('window event: button press')
        self._ui.note_window.present()
        # return True

    def on_note_window_focus_out_event(self, widget, event):
        self._ui.more_popovermenu.popdown()

    def on_note_textview_focus_in_event(self, widget: Gtk.Widget, event: Gdk.EventFocus):
        if not self._note.locked:
            self._ui.note_textview.set_cursor_visible(True)

    def on_note_textview_focus_out_event(self, widget: Gtk.Widget, event: Gdk.EventFocus):
        self._update_note()
        if not self._note.locked:
            self._ui.note_textview.set_cursor_visible(False)
        
    def on_new_button_clicked(self, button: Gtk.Button):
        note = self._context.notes.add_note()
        ui = NoteHandler.attach_ui(self._context, note.uuid)
        ui.show()

    def on_delete_button_clicked(self, window: Gtk.Window):
        self._context.notes.remove_note(self._note.uuid)
        window.close()

    def on_close_button_clicked(self, window: Gtk.Window):
        self._context.notes.set_note_ui(self._note.uuid, None)
        self._note.save()
        window.close()

    def on_more_button_clicked(self, popovermenu: Gtk.PopoverMenu):
        self._ui.note_window.present()
        popovermenu.popup()

    @staticmethod
    def attach_ui(context: TakenoteContext, note_uuid: str) -> NoteUI:
        builder = Gtk.Builder.new_from_file(UIResource.NOTE_WINDOW.get_filename())

        note = context.notes.get_note(note_uuid)
        css_string = note._style.fill_css_template(
            CSSResource.TEMPLATE_NOTE_STYLE.get_filename())

        style_provider = Gtk.CssProvider.new()
        style_provider.load_from_data(css_string.encode("utf-8"))
        ui = NoteUI.from_builder(builder)
        ui.set_style(style_provider)
        context.notes.set_note_ui(note.uuid, ui)

        handler = NoteHandler(context, note.uuid, ui)
        builder.connect_signals(handler)

        return ui
        
    def _toggle_pinning(self, window: Gtk.Window):
        self._note.pinmode = (
            NotePinMode.NONE
            if self._note.pinmode.ispinned
            else NoteHandler.DEFAULT_PINMODE
        )

        self._set_pinning_mode(window)

    def _toggle_pinning_mode(self, window: Gtk.Window):
        # Toggle pinning mode.
        self._note.pinmode = (
            NotePinMode.BELOW
            if self._note.pinmode == NotePinMode.ABOVE
            else NotePinMode.ABOVE
        )

        if self._note.pinmode.ispinned:
            self._set_pinning_mode(window)

    def _set_pinning_mode(self, window: Gtk.Window):
        type_hint = self._note.pinmode.gtk_window_typehint
        window.set_type_hint(type_hint)

        is_pinned = self._note.pinmode.ispinned
        self._ui.move_button.set_sensitive(not is_pinned)
        self._ui.resize_eventbox.set_visible(not is_pinned)
        self._ui.mode_button.set_visible(is_pinned)
        self._update_pinmode_icon()

    def _set_button_icon(self, button: Gtk.Button, icon: TakenoteIcon):
        image = button.get_image()
        if not image:
            image = Gtk.Image.new()
            button.set_image(image)

        self._context.icon_theme.set_screen(Gdk.Screen.get_default())
        pixbuf = self._context.icon_theme.load_icon(icon.value, 16, 0)
        image.set_from_pixbuf(pixbuf)

    def _update_pinmode_icon(self):       
        icon = {
            NotePinMode.ABOVE: TakenoteIcon.FLIP_TO_FRONT,
            NotePinMode.BELOW: TakenoteIcon.FLIP_TO_BACK
        }.get(self._note.pinmode)
        if icon:
            self._set_button_icon(self._ui.mode_button, icon)

    def _update_lock_icon(self):
        icon = TakenoteIcon.LOCK_ENABLED if self._note.locked else TakenoteIcon.LOCK_DISABLED
        self._set_button_icon(self._ui.lock_button, icon)

    def _update_note(self):
        root_x, root_y = self._ui.note_window.get_position()
        width, height = self._ui.note_window.get_size()
        text = self._text_buffer.get_text(
            start=self._text_buffer.get_start_iter(),
            end=self._text_buffer.get_end_iter(),
            include_hidden_chars=False
        )

        self._note.content = text
        self._note.pinmode = self._note.pinmode
        self._note.set_position(root_x, root_y)
        self._note.set_size(height, width)
        self._note.save()
