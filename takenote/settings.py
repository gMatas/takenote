from pkg_resources import resource_filename

from takenote.gi_repository import GIRepository


Gtk = GIRepository.Gtk.load_binding()


class Settings:

    def __init__(self):
        ui_filepath = resource_filename('takenote.resources.ui', 'settings.glade')
        builder = Gtk.Builder.new_from_file(ui_filepath)
        self._window = builder.get_object('settings')

    def show(self):
        return self._window.show()


if __name__ == '__main__':
    Settings().show()
    Gtk.main()
