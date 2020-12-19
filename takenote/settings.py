from takenote.resources.ui import UIResource
from takenote.gi_repository import Gtk


class Settings:

    def __init__(self):
        ui_filepath = resource_filename('takenote.resources.ui', 'settings.glade')
        builder = Gtk.Builder.new_from_file(ui_filepath)
