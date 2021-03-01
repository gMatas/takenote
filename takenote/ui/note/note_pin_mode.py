from enum import Enum

from takenote.gi_repository import GIRepository

Gdk = GIRepository.Gdk.load_binding()


class NotePinMode(Enum):

    NONE: Gdk.WindowTypeHint = Gdk.WindowTypeHint.NORMAL
    ABOVE: Gdk.WindowTypeHint = Gdk.WindowTypeHint.DOCK
    BELOW: Gdk.WindowTypeHint = Gdk.WindowTypeHint.DESKTOP

    @property
    def ispinned(self) -> bool:
        return self != NotePinMode.NONE

    @property
    def gtk_window_typehint(self) -> Gdk.WindowTypeHint:
        return self.value
