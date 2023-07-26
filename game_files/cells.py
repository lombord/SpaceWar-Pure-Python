from weakref import ref


class Cell:
    __slots__ = ('__weakref__', '_current', 'opened')
    _opened = u"\u00B7"

    def __init__(self) -> None:
        self.opened = False
        self._current = ' '

    def open(self):
        self.opened = True
        self._current = self._opened
        return False

    def isOpened(self):
        return self.opened

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return self._current


class BorderCell(Cell):
    _revealed = '*'
    __slots__ = ()

    def reveal(self):
        self.opened = True
        self._current = self._revealed

    def __bool__(self) -> bool:

        return True


class ShipCell(Cell):
    _opened = 'X'
    _unhidden = u'\u25A8'
    __slots__ = ('_ship', 'number')

    def __init__(self, ship, number, hidden=True) -> None:
        super().__init__()
        if not hidden:
            self._current = self._unhidden
        self._ship = ref(ship)
        self.number = number

    @property
    def ship(self):
        return self._ship()

    def open(self):
        super().open()
        self.ship.checkAlive(self.number)
        return True

    def __bool__(self) -> bool:
        return True


if __name__ == '__main__':
    pass
