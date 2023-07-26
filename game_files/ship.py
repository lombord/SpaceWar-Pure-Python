from itertools import product as prod
from weakref import WeakSet as wset, WeakValueDictionary as wValDict, ref


from .cells import BorderCell, ShipCell


class Ship:

    def __init__(self, x, y, isVertical, size, field, num) -> None:
        self.x, self.y = x, y
        self.size = size
        self.isVertical = isVertical
        self._field = ref(field)
        self.num = num
        self.botRef = None
        self.shipCells: wValDict[int, ShipCell] = wValDict()
        self.borderCells: wset[BorderCell] = wset()
        self.__setShip(field)

    @property
    def field(self):
        return self._field()

    def __getShipCoords(self):
        """get correct corrds for the ship"""
        bX, bY = self.x - 1, self.y - 1
        if self.isVertical:
            xEnd, yEnd = bX + 3, bY + self.size + 2
            shipX, shipY = self.x, slice(self.y, self.y + self.size)
        else:
            xEnd, yEnd = bX + self.size + 2, bY + 3
            shipX, shipY = slice(self.x, self.x + self.size), self.y
        return bX, bY, xEnd, yEnd, shipX, shipY

    def __setShip(self, field):
        """set ship on the field"""
        bX, bY, xEnd, yEnd, shipX, shipY = self.__getShipCoords()
        xEnd = xEnd if xEnd <= field.width else field.width
        yEnd = yEnd if yEnd <= field.height else field.height

        for x, y in prod(range(bX, xEnd), range(bY, yEnd)):
            if x >= 0 and y >= 0:
                if not field[y, x]:
                    field[y, x] = BorderCell()
                self.borderCells.add(field[y, x])

        field[shipY, shipX] = [ShipCell(self, num, field._hidden)
                               for num in range(self.size)]

        self.shipCells.update((num, cell) for num, cell in
                              enumerate(field[shipY, shipX]))

    def checkAlive(self, number):
        del self.shipCells[number]
        if not self.shipCells:
            self.revealAll()
            self.field.removeShip(self.num)
            self.callBot()

    def revealAll(self):
        for border in self.borderCells:
            border.reveal()

    def addBotRef(self, bot):
        self.botRef = ref(bot)

    def callBot(self):
        if self.botRef:
            self.botRef().removeShip(self)

    def __bool__(self):
        return bool(self.shipCells)


if __name__ == '__main__':
    pass
