from enum import Enum
from typing import Type

from pkg_resources import resource_filename


class _ResourceLibrary:

    _name: str = None


class BaseResource(_ResourceLibrary, Enum):

    def get_filename(self):
        return resource_filename(self._name, self.value)


def resource_library(name: str):
    def wrap_resource(cls: Type[BaseResource]):
        cls._name = name
        return cls

    return wrap_resource
