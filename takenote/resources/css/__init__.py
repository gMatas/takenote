from takenote.resources.base_resource import BaseResource, resource_library


@resource_library(__package__)
class CSSResource(BaseResource):

    NOTE_STYLE = "note.css"
    TEMPLATE_NOTE_STYLE = "note-template.css.tmp"
