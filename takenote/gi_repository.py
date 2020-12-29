import enum
import importlib
from typing import Any

import gi


class GIRepository(enum.Enum):

    AppIndicator3 = '0.1'
    Gdk = '3.0'
    Gtk = '3.0'

    def __new__(cls, version: str):
        obj = object.__new__(cls)
        obj._value_ = enum.auto()
        return obj

    def __init__(self, version: str):
        gi.require_version(self.name, version)

    def __repr__(self) -> str:
        return '<%s.%s>' % (self.__class__.__name__, self.name)

    def load_binding(self) -> Any:
        binding = importlib.import_module(f'gi.repository.{self.name}')
        return binding
