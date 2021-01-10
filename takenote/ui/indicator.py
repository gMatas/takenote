from typing import Dict, Callable

from takenote.gi_repository import GIRepository
from takenote.notes_collection import NotesCollection
from takenote.ui.note.note_handler import NoteUIHandler


AppIndicator3 = GIRepository.AppIndicator3.load_binding()
Gtk = GIRepository.Gtk.load_binding()


def create_indicator(indicator_id: str, notes: NotesCollection):
    def _on_create_new_note(*args, **kwargs):
        note = notes.add_note()
        note_ui = NoteUIHandler.create_ui(notes, note.uuid)
        note_ui.show()

    def _on_open_settings(*args, **kwargs):
        print("indicator: settings")

    def _on_quit(*args, **kwargs):
        Gtk.main_quit()

    indicator = AppIndicator3.Indicator.new(
        indicator_id,
        "whatever",
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS
    )

    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    menu = Gtk.Menu.new()
    menu_items = [
        _create_menu_item("New Note", {"activate": _on_create_new_note}),
        _create_menu_item("Settings", {"activate": _on_open_settings}),
        _create_menu_item("Quit", {"activate": _on_quit}),
    ]
    for item in menu_items:
        item.show()
        menu.append(item)

    indicator.set_menu(menu)

    return indicator


def _create_menu_item(label: str, signal_handlers: Dict[str, Callable]) -> Gtk.MenuItem:
    menuitem = Gtk.MenuItem.new_with_label(label)
    for signal, handler in signal_handlers.items():
        menuitem.connect(signal, handler)

    return menuitem
