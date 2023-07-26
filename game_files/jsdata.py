import json


class DataBase:
    _fileName = ''

    def __init__(self) -> None:
        self.players = {}
        self.loadPlayers()

    def loadPlayers(self):
        pass

    def __savePlayers(self):
        with open(self._fileName, 'w', encoding='utf-8') as pFile:
            json.dump({player.name: player.toJS()
                      for player in self.players.values()}, pFile, indent=4)

    def savePlayer(self, player):
        self.players[str(player)] = player

    def __getitem__(self, key):
        return self.players[key]

    def __setitem__(self, key, val):
        self.players[key] = val

    def __del__(self):
        self.__savePlayers()

    def __contains__(self, key):
        return key in self.players


if __name__ == '__main__':
    pass
