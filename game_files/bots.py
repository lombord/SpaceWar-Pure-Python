from itertools import product as prod
import os
from pathlib import Path
from random import choice, randrange as rrange, shuffle
import json


from .field import Field
from .player import PlayerBase
from .jsdata import DataBase


class BotData(DataBase):
    _fileName = os.path.join(str(Path(__file__).resolve().parent),
                             'gameData', 'BotsData.json')

    def loadPlayers(self):
        try:
            with open(self._fileName, 'r', encoding='utf-8') as pFile:
                self.players = {name: globals()[name](**data)
                                for name, data in json.load(pFile).items()}
        except Exception as ex:
            return


class BotBase(PlayerBase):

    def __init__(self, wins=0, losses=0) -> None:
        super().__init__(type(self).__name__)
        self.wins = wins
        self.losses = losses

    def updateScores(self, win):
        if win:
            self.wins += 1
            return
        self.losses += 1


class EasyBot(BotBase):

    def __init__(self, wins=0, losses=0) -> None:
        super().__init__(wins, losses)
        self.__combos = None
        self._chance = 1
        self._damagedShips = []

    def toJS(self):
        del self.__combos, self._chance, self._damagedShips
        return super().toJS()

    @property
    def eField(self) -> Field:
        return super().eField

    @eField.setter
    def eField(self, eField):
        PlayerBase.eField.fset(self, eField)
        self.__combos = list(
            prod(range(eField.width), range(eField.height)))
        shuffle(self.__combos)

    def addShip(self, ship):
        if ship and not ship.botRef:
            ship.addBotRef(self)
            self._damagedShips.append(ship)

    def removeShip(self, ship):
        self._damagedShips.remove(ship)

    def openCell(self, cell):
        flag = cell.open()
        flag and self.addShip(cell.ship)
        return flag

    def openRandCell(self):
        coords = self.__combos.pop()
        while self.eField[coords].isOpened():
            coords = self.__combos.pop()
        return self.openCell(self.eField[coords])

    def damageCurrent(self):
        if not self._damagedShips:
            return
        return next(iter(self._damagedShips[0].shipCells.values())).open()

    def __call__(self) -> tuple[int]:
        if rrange(10) < self._chance and self.damageCurrent():
            return True
        return self.openRandCell()


class MediumBot(EasyBot):

    def __init__(self, wins=0, losses=0) -> None:
        super().__init__(wins, losses)
        self._chance = 3


class HardBot(EasyBot):
    def __init__(self, wins=0, losses=0) -> None:
        super().__init__(wins, losses)
        self._chance = 3
        self._shipChance = 1

    def toJS(self):
        del self._shipChance
        return super().toJS()

    def chooseRandShip(self):
        return choice(tuple(self.eField.ships.values()))

    def __call__(self) -> tuple[int]:
        if (not self._damagedShips) and rrange(10) < self._shipChance:
            self.addShip(self.chooseRandShip())
        return super().__call__()


class VeryHardBot(HardBot):

    def __init__(self, wins=0, losses=0) -> None:
        super().__init__(wins, losses)
        self._chance = 10
        self._shipChance = 1


class UnrealBot(VeryHardBot):

    def __init__(self, wins=0, losses=0) -> None:
        super().__init__(wins, losses)
        self._shipChance = 10


if __name__ == '__main__':
    pass
