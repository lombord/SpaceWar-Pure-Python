from itertools import product as prod
from weakref import WeakSet as wset, WeakValueDictionary as WValDict, ref


from .cells import BorderCell, ShipCell


class Ship:

    def __init__(self, x, y, isVertical, size, field, num) -> None:
        self.x, self.y = x, y
        self.size = size
        self.isVertical = isVertical
        self._field = ref(field)
        self.num = num
        self.botRef = None
        self.shipCells: WValDict[int, ShipCell] = WValDict()
        self.borderCells: wset[BorderCell] = wset()
        self.__setShip(field)

    @property
    def field(self):
        return self._field()

    def __getShipCoords(self):
        """get valid coordinates for the ship"""
        field = self.field
        width, height = field.width, field.height
        bX, bY = self.x - 1, self.y - 1
        xSize, ySize = [3, self.size + 2][:: (-1) * (-1 * self.isVertical or 1)]
        xStart, xEnd = max(bX, 0), min(bX + xSize, width)
        yStart, yEnd = max(bY, 0), min(bY + ySize, height)
        if self.isVertical:
            shipX, shipY = self.x, slice(self.y, self.y + self.size)
        else:
            shipX, shipY = slice(self.x, self.x + self.size), self.y
        return xStart, yStart, xEnd, yEnd, shipX, shipY

    def __setShip(self, field):
        """set ship on the field"""
        xStart, yStart, xEnd, yEnd, shipX, shipY = self.__getShipCoords()

        for x, y in prod(range(xStart, xEnd), range(yStart, yEnd)):
            if not field[y, x]:
                field[y, x] = BorderCell()
            self.borderCells.add(field[y, x])

        shipCells = [ShipCell(self, num, field._hidden) for num in range(self.size)]
        field[shipY, shipX] = shipCells

        self.shipCells.update((num, cell) for num, cell in enumerate(shipCells))

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
