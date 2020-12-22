from typing import Dict, Callable

from takenote.constants import APPINDICATOR_ID
from takenote.gi_repository import GIRepository
from takenote.note import Note


AppIndicator3 = GIRepository.AppIndicator3.load_binding()
Gtk = GIRepository.Gtk.load_binding()


def create_indicator():
    indicator = AppIndicator3.Indicator.new(
        APPINDICATOR_ID,
        'whatever',
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS
    )

    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    menu = Gtk.Menu.new()
    menu_items = [
        _create_menu_item('New Note', {'activate': _on_create_new_note}),
        _create_menu_item('Settings', {'activate': _on_open_settings}),
        _create_menu_item('Quit', {'activate': _on_quit}),
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


def _on_create_new_note(menuitem: Gtk.MenuItem):
    note = Note()
    note.show()
    pass


def _on_open_settings(menuitem: Gtk.MenuItem):
    print('indicator: settings')


def _on_quit(menuitem: Gtk.MenuItem):
    Gtk.main_quit()


def main():
    locals()[APPINDICATOR_ID] = create_indicator()
    Gtk.main()


if __name__ == '__main__':
    main()
