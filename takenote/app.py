from typing import Optional

from gi.repository import Gtk

from takenote.constants import APPINDICATOR_ID
from takenote.context import TakenoteContext
from takenote.ui.indicator import create_indicator


class TakenoteApp:

    _instance: Optional["TakenoteApp"] = None

    def __new__(cls):
        if cls._instance:
            return cls._instance

        instance = object.__new__(cls)
        cls._instance = instance

        context = TakenoteContext()
        
        instance._indicator = create_indicator(context, APPINDICATOR_ID)
        instance._indicator_id = APPINDICATOR_ID

        return cls._instance

    def run(self):
        if self._instance:
            Gtk.main()


def main():
    app = TakenoteApp()
    app.run()


if __name__ == "__main__":
    main()
