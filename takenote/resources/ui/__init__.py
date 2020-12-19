import enum
from typing import BinaryIO

from pkg_resources import resource_filename, resource_stream, resource_exists


def _assert_resource_exists(ui_resource_method):
    def wrapped_ui_resource_method(self):
        if resource_exists(__package__, self.value):
            return ui_resource_method(self)

        raise FileNotFoundError(
            f'Resource {repr(self)} not found at '
            f'{resource_filename(__package__, self.value)}.')

    return wrapped_ui_resource_method


class UIResource(enum.Enum):

    NOTE = 'note.glade'
    SETTINGS = 'settings.glade'

    @_assert_resource_exists
    def get_filepath(self) -> str:
        return resource_filename(__package__, self.value)

    @_assert_resource_exists
    def get_stream(self) -> BinaryIO:
        return resource_stream(__package__, self.value)
