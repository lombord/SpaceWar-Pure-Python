import os
from re import IGNORECASE, compile
from string import ascii_lowercase as aLower
from bisect import bisect_left as bLeft
from weakref import ref
import json
from pathlib import Path

from .jsdata import DataBase
from .field import Field
from .settings import Settings


class PlayerData(DataBase):
    _fileName = os.path.join(str(Path(__file__).resolve().parent),
                             'gameData', 'PlayersData.json')

    def loadPlayers(self):
        try:
            with open(self._fileName, 'r', encoding='utf-8') as pFile:
                self.players = {name: Player(name=name, **data)
                                for name, data in json.load(pFile).items()}
        except Exception:
            return


class PlayerBase:

    def __init__(self, name: str) -> None:
        self.name = name
        self.__eField = None  # enemyField

    def updateScores(self, win):
        pass

    @property
    def eField(self) -> Field:
        return self.__eField()

    @eField.setter
    def eField(self, enemyField):
        self.__eField = ref(enemyField)

    def __str__(self) -> str:
        return self.name

    def toJS(self):
        del self.__eField, self.name
        return self.__dict__

    @classmethod
    def fromDict(cls, dct):
        return cls(**dct)


class Player(PlayerBase):

    inputPattern = compile(
        r'\s*(?:([a-z])\s*(\d{1,2})|(\d{1,2})\s*([a-z]))\s*', IGNORECASE)

    def __init__(self, name: str, easy=0, medium=0, hard=0,
                 veryHard=0, unreal=0, settings=None) -> None:
        super().__init__(name)
        self.easy, self.medium, self.hard, self.veryHard, self.unreal = easy, medium, hard, veryHard, unreal

        if settings is None:
            self.settings = Settings()
        else:
            self.settings = Settings(**settings)

    def toJS(self):
        tmp = dict(super().toJS())
        tmp['settings'] = tmp['settings'].toJS()
        return tmp

    def updateScores(self, win):
        self.__dict__[self.settings.gameMode] += win or -1

    def resetScores(self):
        self.easy = self.medium = self.hard = self.veryHard = self.unreal = 0

    def __getCorrectInput(self):
        """"""
        result = input(f"{self.name} Enter coords(col, row): ")
        result = self.inputPattern.fullmatch(result)
        while not result:
            print('Incorrect input! Try again')
            result = input(f"\n{self.name}Enter coords(col, row): ")
            result = self.inputPattern.fullmatch(result)
        result = result.groups()
        return result[:2] if result[1] else result[-1:-3:-1]

    def __call__(self) -> tuple[int]:
        x, y = self.__getCorrectInput()
        x, y = bLeft(aLower, x.lower()), int(y) - 1
        while True:
            try:
                if self.eField[y, x].isOpened():
                    raise IndexError
            except IndexError:
                print('Incorrect input! Try again')
                x, y = self.__getCorrectInput()
                x, y = bLeft(aLower, x), int(y) - 1
            else:
                break
        return self.eField[y, x].open()


if __name__ == '__main__':
    pass
