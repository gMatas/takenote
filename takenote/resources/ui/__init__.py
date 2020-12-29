from takenote.resources.base_resource import BaseResource, resource_library


@resource_library(__package__)
class UIResource(BaseResource):

    NOTE_WINDOW = 'note.glade'
    SETTINGS_WINDOW = 'settings.glade'
