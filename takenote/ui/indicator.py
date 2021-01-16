from typing import Callable, Dict

from takenote.gi_repository import GIRepository
from takenote.notes_collection import NotesCollection
from takenote.ui.note.note_handler import NoteHandler

AppIndicator3 = GIRepository.AppIndicator3.load_binding()
Gtk = GIRepository.Gtk.load_binding()


def create_indicator(indicator_id: str, notes: NotesCollection):
    
    def _on_create_new_note(*args, **kwargs):
        note = notes.add_note()
        _show_note_ui(notes, note.uuid)

    def _on_show_all_notes(*args, **kwargs):
        for note_uuid in notes.uuids:
            _show_note_ui(notes, note_uuid)

    def _on_open_settings(*args, **kwargs):
        print("indicator: settings")

    def _on_quit(*args, **kwargs):
        Gtk.main_quit()

    indicator = AppIndicator3.Indicator.new(
        indicator_id,
        "note",
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS
    )

    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    menu = Gtk.Menu.new()
    menu_items = [
        _new_menu_item("New Note", {"activate": _on_create_new_note}),
        _new_menu_item("Show All", {"activate": _on_show_all_notes}),
        _new_menu_item("Settings", {"activate": _on_open_settings}),
        _new_menu_item("Quit", {"activate": _on_quit}),
    ]
    for item in menu_items:
        item.show()
        menu.append(item)

    indicator.set_menu(menu)

    return indicator


def _show_note_ui(notes: NotesCollection, note_uuid: str):
    if notes.get_note_ui(note_uuid):
        return
    
    note_ui = NoteHandler.attach_ui(notes, note_uuid)
    note_ui.show()


def _new_menu_item(label: str, signal_handlers: Dict[str, Callable]) -> Gtk.MenuItem:
    menuitem = Gtk.MenuItem.new_with_label(label)
    for signal, handler in signal_handlers.items():
        menuitem.connect(signal, handler)

    return menuitem
