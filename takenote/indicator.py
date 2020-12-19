from typing import Dict, Callable

from takenote.gi_repository import Gtk, AppIndicator3
from takenote.note import Note


class IndicatorHandler:

    APPINDICATOR_ID = 'takenote-indicator'

    def __init__(self):
        indicator = AppIndicator3.Indicator.new(
            IndicatorHandler.APPINDICATOR_ID,
            'whatever',
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES
        )

        indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        menu = Gtk.Menu.new()
        menu_items = [
            _create_menu_item('New Note', {'activate': self.on_create_new_note}),
            _create_menu_item('Settings', {'activate': self.on_open_settings}),
            _create_menu_item('Quit', {'activate': self.on_quit}),
        ]
        for item in menu_items:
            item.show()
            menu.append(item)

        indicator.set_menu(menu)

    def on_create_new_note(self, menuitem: Gtk.MenuItem):
        note = Note()
        note.show()

    def on_open_settings(self, menuitem: Gtk.MenuItem):
        print('indicator: settings')

    def on_quit(self, menuitem: Gtk.MenuItem):
        Gtk.main_quit()


def _create_menu_item(label: str, signalhandlers: Dict[str, Callable]) -> Gtk.MenuItem:
    menuitem = Gtk.MenuItem.new_with_label(label)
    for signal, handler in signalhandlers.items():
        menuitem.connect(signal, handler)

    return menuitem
