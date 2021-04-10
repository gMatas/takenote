from enum import Enum

from gi.repository import Gdk


class NotePinMode(Enum):

    NONE: Gdk.WindowTypeHint = Gdk.WindowTypeHint.UTILITY
    ABOVE: Gdk.WindowTypeHint = Gdk.WindowTypeHint.DOCK
    BELOW: Gdk.WindowTypeHint = Gdk.WindowTypeHint.DESKTOP

    @property
    def ispinned(self) -> bool:
        return self != NotePinMode.NONE

    @property
    def gtk_window_typehint(self) -> Gdk.WindowTypeHint:
        return self.value
