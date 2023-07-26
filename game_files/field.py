from itertools import product as prod
from numpy import array, ndarray
from random import randrange as rrange
from string import ascii_uppercase as aUpper

from .cells import Cell
from .ship import Ship


class Field:

    # initialization methods
    def __init__(self, width, height, hidden=True, maxSize=None) -> None:
        self.width = width
        self.height = height
        self._hidden = hidden
        self.__setSize(maxSize)
        self.__fillField()
        self.genShips()

    def __setSize(self, maxSize):
        """Set available size of the ships"""
        if maxSize is None or maxSize*2 > min(self.width, self.height):
            maxSize = min(self.width, self.height)//2
        self.__sizes = sum(((i,)*(maxSize - i)
                           for i in range(1, maxSize)), start=())

    def __fillField(self):
        """Fill the field with cells"""
        self.field: ndarray[Cell] = array([[Cell() for _ in range(self.width)]
                                          for _ in range(self.height)])
        self.ships = {}
    # end

    # gen methods
    def genShips(self):
        """Generate ships by given sizes"""
        for n, size in enumerate(reversed(self.__sizes)):
            if not self.__genShip(size, n):
                self.__fillField()
                break
        else:
            return
        self.genShips()

    def __genShip(self, size, n):
        """Generate ship by given size"""
        count = 0
        while True:
            x, y, check, isVert = self.__randDir(size)
            if all(not self[y, x] for x, y in check):
                self.ships[n] = Ship(x, y, isVert, size, self, n)
                return True
            count += 1
            if count >= self.width * self.height:
                return False

    def __randDir(self, size):
        """Get random direction and coordinates for given size"""
        isVert = rrange(2)
        if isVert:
            x = rrange(self.width)
            y = rrange(self.height - size + 1)
            check = prod([x], range(y, y + size))
        else:
            x = rrange(self.width - size + 1)
            y = rrange(self.height)
            check = prod(range(x, x + size), [y])
        return x, y, check, isVert
    # end

    # render methods
    def show(self):
        """Show field"""
        print(self)

    @classmethod
    def renderParallel(cls, *fields, sepSize=10):
        """Renders fields parallel"""
        print()
        for rows in zip(*map(cls.__printMap, fields)):
            print(*rows, sep=' '*sepSize)

    def __printMap(self):
        """Additional method to renderParallel"""
        yield ' '*5 + '   '.join(aUpper[:self.width]) + ' '*2
        rSep = '   %s' % (u'\u2014'*(self.width*4 + 1))
        cSep = '|'

        for n, row in enumerate(self, 1):
            yield rSep
            yield f'{n:<3}{cSep:<2}' + ' | '.join(map(str, row)) + f'{cSep:>2}'
        yield rSep

    def __str__(self) -> str:
        """Shows field"""
        letters = ' '*5 + '   '.join(aUpper[:self.width])
        rSep = '\n   %s\n' % (u'\u2014'*(self.width*4 + 1))
        cSep = '|'
        field = rSep + rSep.join(f'{n:<3}{cSep:<2}' + ' | '.join(map(str, row)) + f'{cSep:>2}'
                                 for n, row in enumerate(self, 1)) + rSep
        return f'{letters}{field}'
    # end

    # iter methods
    def __iter__(self):
        """get iterator of the field"""
        return iter(self.field)

    def __getitem__(self, cords) -> Cell:
        """get ceel by given coords"""
        return self.field[cords]

    def __setitem__(self, cords, val) -> None:
        """set ceel by given coords"""
        self.field[cords] = val

    def __len__(self) -> int:
        return len(self.field)
    # end

    # boolean methods
    def __bool__(self) -> bool:
        return bool(self.ships)

    def removeShip(self, num):
        del self.ships[num]


if __name__ == '__main__':
    pass
