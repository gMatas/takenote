from takenote.gi_repository import Gtk
from takenote.indicator import IndicatorHandler


def start():
    IndicatorHandler()
    Gtk.main()


if __name__ == '__main__':
    start()
