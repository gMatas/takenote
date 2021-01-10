from takenote.gi_repository import GIRepository
from takenote.resources.ui import UIResource


Gtk = GIRepository.Gtk.load_binding()


class Settings:

    def __init__(self):
        ui_filepath = UIResource.SETTINGS_WINDOW.get_filename()
        builder = Gtk.Builder.new_from_file(ui_filepath)
        self._window = builder.get_object("settings")

    @classmethod
    def show_window(cls):
        cls().show()

    def show(self):
        return self._window.show()


if __name__ == "__main__":
    Settings.show_window()
    Gtk.main()
