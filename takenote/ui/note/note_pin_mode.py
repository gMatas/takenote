import enum

from takenote.gi_repository import GIRepository


Gdk = GIRepository.Gdk.load_binding()


class NotePinMode(enum.Enum):

    ABOVE: Gdk.WindowTypeHint = Gdk.WindowTypeHint.DOCK
    BELOW: Gdk.WindowTypeHint = Gdk.WindowTypeHint.DESKTOP
    NONE: Gdk.WindowTypeHint = Gdk.WindowTypeHint.UTILITY

    @property
    def ispinned(self) -> bool:
        return self != NotePinMode.NONE

    @property
    def gtk_window_typehint(self) -> Gdk.WindowTypeHint:
        return self.value
